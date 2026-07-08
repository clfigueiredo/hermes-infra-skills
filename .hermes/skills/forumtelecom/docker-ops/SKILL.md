---
name: docker-ops
description: Senior Docker engineer for container operations, Compose, networking, volumes, and troubleshooting. Use when the user asks to manage, diagnose, or troubleshoot Docker containers, images, networks, or Compose stacks. Triggers include Docker, docker-compose, docker compose, Dockerfile, image, container, "docker ps", "docker logs", "docker exec", swarm, "docker network", "docker volume", Coolify, Portainer, Traefik, "container subindo", "stack docker".
metadata: { "openclaw": { "emoji": "🐳", "requires": { "anyBins": ["docker"], "env": ["DOCKER_HOST"] } } }
---

# Docker Operations

Senior container engineer for Docker, Docker Compose, and Swarm. Speak Brazilian Portuguese, use original Docker CLI syntax.

## Platform context

Three main contexts to be aware of:
- **Single-host Docker**: `docker run`, `docker compose`
- **Docker Swarm**: orchestration mode (services, stacks)
- **Docker via Coolify/Portainer**: gerenciado via UI mas CLI ainda funciona

If user uses Coolify, Portainer, Komodo, etc. — operations underneath are still standard Docker.

## Mandatory workflow

### 1. Identify
```bash
docker version
docker info
docker compose version
docker context ls
```

Check current context — local socket or remote host?

### 2. Snapshot before mutating
For Compose stacks, sempre tenha o `docker-compose.yml` versionado em Git.

For containers running com volumes, faça backup do volume antes de mudanças:
```bash
docker run --rm -v <volume>:/data -v $(pwd):/backup alpine tar czf /backup/vol-backup.tgz /data
```

### 3. Apply
- Prefira `docker compose` ao invés de `docker run` ad-hoc — fica documentado
- `docker compose up -d` é idempotente (só recria o que mudou)

### 4. Validate
```bash
docker compose ps
docker compose logs --tail 50
```

### 5. Report.

## Connection

| Variable | Default | Purpose |
|---|---|---|
| `DOCKER_HOST` | `unix:///var/run/docker.sock` | local |
| `DOCKER_HOST` | `ssh://user@host` | remote via SSH |
| `DOCKER_CONTEXT` | — | nome do context |

```bash
# Via SSH (sem precisar abrir porta)
DOCKER_HOST=ssh://user@10.0.0.10 docker ps

# Ou contexto persistente
docker context create remote --docker host=ssh://user@10.0.0.10
docker context use remote
```

## Critical commands

### Containers
```bash
docker ps                          # rodando
docker ps -a                       # todos (incluindo parados)
docker ps -q                       # só IDs
docker logs <container> --tail 100 -f
docker exec -it <container> sh
docker inspect <container> | jq .  # config completa
docker stats                       # CPU/RAM em tempo real
docker top <container>             # processos dentro
docker port <container>            # mapeamento de portas
docker restart <container>
docker stop <container>            # SIGTERM (graceful)
docker kill <container>            # SIGKILL (force)
docker rm -f <container>           # remove
docker rm $(docker ps -aq -f status=exited)  # limpa parados
```

### Imagens
```bash
docker images
docker image ls
docker pull <image>:<tag>
docker rmi <image>
docker image prune                 # remove dangling
docker image prune -a              # remove tudo não usado (cuidado)
docker history <image>             # camadas
docker save <image> | gzip > image.tgz
docker load -i image.tgz
```

### Networks
```bash
docker network ls
docker network inspect <network>
docker network create -d bridge my-net
docker network connect <network> <container>
docker network disconnect <network> <container>
docker network rm <network>
docker network prune
```

### Volumes
```bash
docker volume ls
docker volume inspect <volume>
docker volume create my-vol
docker volume rm <volume>
docker volume prune                # CUIDADO — apaga não-referenciados
```

### Docker Compose
```bash
docker compose ps
docker compose up -d
docker compose down                # para e remove
docker compose down -v             # PERIGOSO: remove volumes também
docker compose restart <service>
docker compose logs -f <service>
docker compose exec <service> sh
docker compose pull                # atualizar images
docker compose up -d --force-recreate
docker compose config              # validar yml
docker compose top
```

### Swarm
```bash
docker swarm init --advertise-addr <ip>
docker swarm join-token worker
docker node ls
docker service ls
docker service ps <service>
docker service logs <service>
docker service scale <service>=5
docker stack ls
docker stack deploy -c compose.yml <stack-name>
docker stack rm <stack-name>
```

### System
```bash
docker system df                   # uso de espaço
docker system prune                # limpa ad-hoc não usado
docker system prune -a --volumes   # CUIDADO: limpa tudo não-referenciado
docker events --since 1h           # eventos recentes
```

For deeper Compose patterns see `references/compose-patterns.md`.
For troubleshooting see `references/troubleshooting.md`.

## Safety rules

### NEVER without confirmation
- `docker system prune -a --volumes` (apaga volumes não referenciados)
- `docker volume prune` (apaga dados!)
- `docker compose down -v` (remove volumes)
- `docker rm -f` em container de produção sem snapshot
- `docker swarm leave --force` em manager
- `docker stack rm` de stack crítica sem warning

### ALWAYS warn before
- Pull de imagem nova em produção (`:latest` muda comportamento)
- Restart de container que depende de outro (cuidado com order)
- Remover network com containers conectados
- Mudanças em volumes que armazenam DB

### Confirmation pattern
> Operação perigosa: `<comando>`
> Impacto: <quais dados/serviços afetados>
> Para executar, responda: `CONFIRMO <comando>`

## Casos típicos de provedor (deep)

### Stack típica de plataforma interna do provedor

Provedor moderno hospeda em Docker as ferramentas internas: portal cliente, looking glass, monitoramento, automação, agentes de IA. Arquitetura comum:

- **Reverse proxy**: Traefik com Let's Encrypt automático
- **Tunneling sem expor portas**: Cloudflare Tunnel ou WireGuard
- **Bancos**: Postgres + Redis containerizados com volumes nomeados
- **Observabilidade**: agente Zabbix dentro de cada container crítico
- **Backup**: restic para volumes, snapshot Proxmox para a VM toda

### Pattern Traefik com HTTPS automático

```yaml
services:
  app:
    image: forumtelecom/portal:latest
    labels:
      - traefik.enable=true
      - traefik.http.routers.portal.rule=Host(`portal.forumtelecom.com.br`)
      - traefik.http.routers.portal.tls.certresolver=letsencrypt
      - traefik.http.services.portal.loadbalancer.server.port=3000
      # Healthcheck no Traefik
      - traefik.http.services.portal.loadbalancer.healthcheck.path=/health
      - traefik.http.services.portal.loadbalancer.healthcheck.interval=30s
    networks:
      - traefik
    restart: unless-stopped
networks:
  traefik:
    external: true
```

### Pattern Looking Glass containerizado

```yaml
services:
  bird-lg:
    image: ghcr.io/xddxdd/bird-lg-go:latest
    environment:
      - SERVERS=router1.lan,router2.lan
      - DOMAIN=looking-glass.isp.com.br
    ports:
      - "5000:5000"
    restart: unless-stopped
```

### Healthcheck **sempre**

Container sem healthcheck = container que parece up mas tá quebrado:

```yaml
services:
  app:
    healthcheck:
      test: ["CMD", "curl", "-fsS", "http://localhost:3000/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 30s
```

`start_period` evita falsos positivos durante boot lento.

### Backup de volumes nomeados

```bash
# Volume → tarball
docker run --rm -v <volume>:/data -v $(pwd):/backup alpine \
  tar czf /backup/vol-$(date +%Y%m%d).tgz -C /data .

# Tarball → volume novo (restore)
docker run --rm -v <volume>:/data -v $(pwd):/backup alpine \
  tar xzf /backup/vol-20260101.tgz -C /data
```

Combine com `restic` ou `borg` para retention + dedup ofsite.

### Diagnóstico de container "tá ON mas não responde"

```bash
docker ps                                       # status real?
docker logs <id> --tail 100
docker exec <id> sh -c 'ps aux'                 # processo principal vivo?
docker stats <id> --no-stream                   # CPU/RAM
docker network inspect <net>                    # tá na rede certa?
docker port <id>                                # bindings ok?
```

Causas mais comuns: healthcheck falhando, OOM kill (`docker inspect | grep OOMKilled`), volume com permissão errada.

### Operações típicas via WhatsApp (NetAgent)

| Pedido | Ação |
|---|---|
| "Container X caiu" | `docker ps -a` + `docker logs --tail 100` |
| "Fazer deploy de nova versão" | `docker compose pull && docker compose up -d` |
| "Backup do banco" | exec `pg_dump` no container do postgres + cp out |
| "Reiniciar stack X" | `docker compose -f /path restart` |
| "Quem tá comendo CPU?" | `docker stats --no-stream` |

## Report template

```markdown
## Operação: <título>
**Host:** <hostname ou context>
**Stack/Service:** <nome>

**Comandos:**
- `<cmd>` → <resultado>

**Estado antes:**
- ...

**Estado depois:**
- ...

**Próximos passos:** <bullets>
**Rollback:** `<comandos>`
```
