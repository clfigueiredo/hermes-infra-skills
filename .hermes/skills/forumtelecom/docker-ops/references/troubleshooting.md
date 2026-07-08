# Docker — Troubleshooting comum

## Container não sobe

```bash
docker logs <container> --tail 100
docker inspect <container> | jq '.[0].State'
```

State possíveis:
- `created` — criado mas nunca rodou (problema na imagem ou comando)
- `exited` — rodou e saiu (ver exit code)
- `dead` — Docker não consegue gerenciar mais (raro, geralmente filesystem corrompido)
- `restarting` — tá em loop de restart (ver logs e healthcheck)

Exit codes comuns:
| Code | Significado |
|---|---|
| 0 | Saiu normalmente |
| 1 | Erro genérico |
| 125 | Erro do daemon Docker |
| 126 | Comando não executável |
| 127 | Comando não encontrado |
| 137 | Killed (OOM ou SIGKILL) |
| 143 | SIGTERM normal |

## Container faz restart loop

```bash
docker logs <container> --tail 200 -f
docker events --filter container=<container>
```

Causas frequentes:
- Healthcheck falha → `unhealthy` → restart policy puxa
- App crasha imediatamente → ver logs
- Faltando env var → app sai com erro
- Volume com permissão errada → app não escreve

Para parar o loop temporariamente:
```bash
docker update --restart=no <container>
docker stop <container>
# investiga, corrige, depois:
docker update --restart=unless-stopped <container>
docker start <container>
```

## OOM (Out of Memory)

```bash
dmesg | grep -i "killed process"
docker inspect <container> | jq '.[0].State.OOMKilled'
```

Soluções:
- Aumentar limit: `docker update --memory 1g --memory-swap 1g <container>`
- Investigar leak na app
- Reduzir concorrência

## Sem espaço em disco

```bash
docker system df
df -h
du -sh /var/lib/docker
```

Limpeza segura (não toca em volumes nomeados ou containers vivos):
```bash
docker system prune
docker image prune -a
docker builder prune -a       # cache de build
```

Limpeza agressiva (cuidado!):
```bash
docker system prune -a --volumes
```

## Network não conecta

```bash
docker network inspect <network>
docker exec <container> ip a
docker exec <container> ping <other-container>
docker exec <container> nslookup <other-container>
```

Containers no mesmo Compose se enxergam pelo nome do service. Em networks diferentes, precisam ser conectados explicitamente.

```bash
docker network connect <network> <container>
```

## Volumes — permissões erradas

Erro comum: app dentro do container roda como user non-root, mas volume foi criado como root.

```bash
docker exec <container> id
ls -la /var/lib/docker/volumes/<volume>/_data
```

Fix:
```bash
docker exec --user root <container> chown -R 1000:1000 /app/data
```

Ou no Dockerfile:
```dockerfile
USER 1000
```

Ou no compose:
```yaml
services:
  app:
    user: "1000:1000"
```

## Imagem não baixa

```bash
docker pull <image>:<tag>
# Erro auth → docker login
# Rate limit → docker login (5K pulls/dia anônimo no Docker Hub)
# Network → verificar DNS, proxy
```

Para registry self-hosted ou privado:
```bash
docker login <registry-url>
```

## Build lento ou falhando

```bash
# Cache rebuild
docker build --no-cache -t my/app .

# Ver camadas pesadas
docker history my/app

# Build com BuildKit (mais rápido, melhor cache)
DOCKER_BUILDKIT=1 docker build .
```

Multi-stage build pra reduzir tamanho final:
```dockerfile
FROM node:20 AS builder
WORKDIR /app
COPY . .
RUN npm ci && npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

## Logs gigantes (encheram disco)

```bash
ls -lh /var/lib/docker/containers/*/{*-json.log}
```

Truncar em emergência:
```bash
truncate -s 0 /var/lib/docker/containers/<id>/<id>-json.log
```

Solução permanente — adicionar `logging.options.max-size` no compose ou em `/etc/docker/daemon.json`:
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```
Reiniciar Docker depois: `systemctl restart docker`.

## Performance lenta (alta CPU/IO)

```bash
docker stats
iotop -o
```

Causas:
- Volume bind-mount em filesystem lento (NFS, SSHFS)
- Container sem cpu/memory limits — disputa de recursos
- Logs sendo flushados constantemente (driver síncrono)

## Permissão SSH para Docker remoto

Com `DOCKER_HOST=ssh://...`:
```bash
# Testar
ssh user@host docker ps

# Adicionar user ao grupo docker no host remoto
sudo usermod -aG docker user
# logout/login
```

## Daemon não inicia

```bash
journalctl -u docker -n 100
systemctl status docker
docker info
```

Soluções comuns:
- `/var/lib/docker` corrompido — backup e reinstalação
- Conflito com outro container runtime (containerd, podman)
- Socket file faltando

## Comandos úteis para debugging profundo

```bash
# Inspecionar processo dentro do container
docker exec <container> ps auxf

# Tcpdump dentro do container
docker run --rm --net container:<container> nicolaka/netshoot tcpdump -i any

# Strace
docker exec <container> strace -p <pid>

# Filesystem do container (snapshot)
docker diff <container>

# Copiar arquivos
docker cp <container>:/path/file ./local-file
docker cp ./local-file <container>:/path/
```
