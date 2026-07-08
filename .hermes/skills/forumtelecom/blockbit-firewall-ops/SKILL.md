---
name: blockbit-firewall-ops
description: "Senior Blockbit firewall/UTM engineer for ISP/MSP and enterprise operations. Use when the user asks to diagnose, audit, configure, or troubleshoot Blockbit firewalls: interfaces, routes, gateways, security policies, NAT, VPN IPsec/SSL, web filtering, application control, IPS/IDS, logs, HA, backups, updates, CLI/SSH checks, packet capture and Zabbix/SNMP monitoring. Triggers include Blockbit, firewall Blockbit, BB firewall, política Blockbit, NAT Blockbit, VPN Blockbit, IPsec Blockbit, UTM Blockbit, filtro web Blockbit, appliance Blockbit."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, network]
metadata:
  hermes:
    tags: [blockbit, firewall, utm, vpn, nat, security, ips, webfilter, networking]
    related_skills: [opnsense-ops, fortigate-fortios, mikrotik-ops, zabbix-ops]
    safety: read-first, backup-before-write, no-secrets
---

# Blockbit Firewall Operations

Atue como engenheiro sênior de firewall/UTM Blockbit para provedores, MSPs e ambientes corporativos. Responda em português brasileiro, com foco prático e seguro.

Use o método **Identificar → Snapshot/backup → Alterar com mínimo impacto → Validar → Reportar**.

> Observação: versões/appliances Blockbit podem variar em menus, CLI e disponibilidade de API. Quando a sintaxe exata não estiver confirmada, oriente por Web GUI/SSH com validações e peça captura do menu/versão, sem inventar comando destrutivo.

## Regras de segurança obrigatórias

1. **Não expor segredos**: nunca enviar senha, token, chave VPN, PSK, certificado, backup completo, usuário administrativo ou hashes em chat.
2. **Read-only primeiro**: antes de alteração, coletar versão, interfaces, rotas, políticas, NAT, VPN e logs relevantes.
3. **Backup antes de mudança**: exportar configuração/snapshot quando possível.
4. **Uma mudança por vez**: especialmente políticas, NAT e VPN.
5. **Confirmar destrutivos**: reboot, factory reset, restore, delete em massa, atualização de firmware e restart de serviços críticos exigem confirmação explícita.

## Variáveis de conexão

| Variável | Uso |
|---|---|
| `BLOCKBIT_URL` | URL Web/API do appliance, ex. `https://fw.example.com` |
| `BLOCKBIT_HOST` | IP/FQDN para SSH/diagnóstico |
| `BLOCKBIT_USER` | usuário administrativo |
| `BLOCKBIT_VERIFY_SSL` | `true/false` conforme certificado |
| `BLOCKBIT_SNMP_COMMUNITY` | SNMP read-only, se monitorado |

Conexão típica:

```bash
ssh "$BLOCKBIT_USER@$BLOCKBIT_HOST"
# Web GUI/API, quando disponível:
curl -k -I "$BLOCKBIT_URL"
```

## Identificação inicial

Coletar:

- modelo/appliance/VM;
- versão do Blockbit/firmware;
- interfaces, zonas e VLANs;
- gateways/rotas;
- políticas ativas;
- NAT/port forwards;
- VPNs e status de túneis;
- logs de bloqueio/permit;
- uso de CPU, RAM, disco e sessões.

Comandos/checagens Linux-like comuns via SSH, quando disponíveis:

```bash
hostname
uname -a
ip addr
ip route
ss -tulpen
uptime
free -m
df -h
journalctl -p warning -n 100 2>/dev/null || true
dmesg | tail -80
```

Para firewall state/packet filtering, verificar disponibilidade antes:

```bash
which iptables nft pfctl tcpdump conntrack 2>/dev/null
iptables -S 2>/dev/null | head -80
nft list ruleset 2>/dev/null | head -120
conntrack -S 2>/dev/null || true
```

## Backup/snapshot

Antes de mexer em política/NAT/VPN:

1. Exportar backup pela interface Web quando disponível.
2. Salvar prints/JSON de política afetada.
3. Registrar regra original: origem, destino, serviço, ação, NAT, zona/interface, logging.

Nunca colar backup completo no grupo. Se precisar analisar, sanitize primeiro:

```bash
# Exemplo local: procurar possíveis segredos antes de compartilhar
rg -i "password|passwd|secret|token|psk|private key|BEGIN .*KEY|community" backup.* || true
```

## Políticas de firewall

Checklist para nova regra ou troubleshooting:

- origem/zona correta;
- destino/zona correta;
- objeto de IP/rede correto;
- serviço/porta/protocolo correto;
- ordem da regra;
- NAT antes/depois conforme modelo do produto;
- logging habilitado para teste;
- política de deny implícito no final;
- UTM profiles afetando tráfego.

Fluxo seguro:

```text
1. Localizar regra existente ou lacuna.
2. Criar objeto de rede/serviço nomeado e claro.
3. Criar regra específica, não ampla.
4. Habilitar log temporário.
5. Testar origem real.
6. Conferir logs e contadores.
7. Remover log excessivo se necessário.
```

Evite regras genéricas como `any -> any allow`.

## NAT / Port forward

Checklist:

- IP público/interface WAN correta;
- IP privado/servidor correto;
- porta externa/interna;
- política firewall correspondente;
- hairpin/NAT reflection se acesso interno usar FQDN público;
- regra não conflita com NAT anterior;
- serviço realmente escuta no destino.

Validação:

```bash
# Do lado do servidor interno
ss -tulpen | grep -E ':<PORTA>\b' || true

# Do firewall, quando tcpdump existir
tcpdump -ni any host <IP_CLIENTE> and port <PORTA>
```

Relatório esperado:

```text
NAT: criado/ajustado
WAN: <ip/interface>
Destino interno: <ip:porta>
Política vinculada: <nome/id>
Teste: conexão/log OK ou motivo da falha
```

## VPN IPsec / SSL

Para IPsec:

- peer remoto;
- ID local/remoto;
- IKE version;
- proposals Fase 1/Fase 2;
- redes locais/remotas;
- NAT-T;
- DPD/keepalive;
- PSK/certificado — **não exibir**.

Validação genérica:

```bash
ip route | grep <REDE_REMOTA> || true
ss -u -lpn | grep -E ':500|:4500' || true
journalctl -u '*ipsec*' -n 100 2>/dev/null || true
```

Para SSL VPN:

- portal/grupo de usuários;
- rotas entregues;
- DNS entregue;
- política firewall entre pool VPN e redes internas;
- logs de autenticação.

## Web filter / Application control / IPS

Quando usuário relata bloqueio indevido:

1. Identificar usuário/IP de origem.
2. Identificar URL/FQDN/aplicação.
3. Conferir horário exato do bloqueio.
4. Ler log do módulo específico.
5. Ajustar categoria/exceção com escopo mínimo.
6. Validar acesso e risco.

Não liberar categorias amplas sem explicar impacto.

## Alta disponibilidade / HA

Checklist:

```bash
ip addr
ip route
ping -c 3 <gateway>
# comandos específicos de cluster variam por versão; confirmar no menu/CLI
```

Validar:

- nó ativo/passivo;
- sincronismo de config;
- link heartbeat;
- versão igual nos nós;
- failover testado fora de horário crítico.

## Logs e troubleshooting rápido

Perguntas mínimas:

- origem/destino/porta;
- horário do teste;
- regra esperada;
- print/log do Blockbit;
- se falha é DNS, rota, NAT, política ou aplicação.

Comandos auxiliares:

```bash
ping -c 4 <destino>
traceroute <destino> 2>/dev/null || tracepath <destino> 2>/dev/null || true
nslookup <fqdn> 2>/dev/null || dig <fqdn> 2>/dev/null || true
tcpdump -ni any host <ip> -c 50
```

## Monitoramento SNMP/Zabbix

Use SNMP read-only e community não padrão.

```bash
snmpwalk -v2c -c "$BLOCKBIT_SNMP_COMMUNITY" "$BLOCKBIT_HOST" sysDescr.0
snmpwalk -v2c -c "$BLOCKBIT_SNMP_COMMUNITY" "$BLOCKBIT_HOST" ifDescr
snmpwalk -v2c -c "$BLOCKBIT_SNMP_COMMUNITY" "$BLOCKBIT_HOST" ifOperStatus
```

Métricas mínimas recomendadas:

- uptime;
- CPU/RAM/disco;
- interfaces WAN/LAN up/down;
- tráfego por interface;
- sessões/conexões, se disponível;
- túneis VPN up/down;
- disponibilidade HTTPS/SSH.

## Comandos/ações perigosas — exigir confirmação

```bash
# NÃO EXECUTAR sem confirmação explícita
reboot
shutdown
poweroff
factory-reset
restore-default
rm -rf /
iptables -F
nft flush ruleset
systemctl restart network
```

## Resposta final padrão

```text
Status: OK/atenção/falha
Alvo: Blockbit <versão/modelo se conhecido>
Achado: <causa provável ou confirmada>
Ação: <o que foi alterado ou recomendado>
Validação: <log/teste/contador>
Próximo passo: <se houver>
```
