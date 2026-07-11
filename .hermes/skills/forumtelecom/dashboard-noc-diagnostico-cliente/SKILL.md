---
name: dashboard-noc-diagnostico-cliente
description: "Use when building or operating a NOC dashboard where a technician enters a customer's PPPoE login and Hermes performs read-only diagnostics: PPPoE status/IP/uptime/disconnect logs, AP/radio signal and CCQ, AP port/cable errors, DNS resolution time, HTTP latency to META/social networks, health opinion and technical report."
version: 1.0.0
author: Hermes Tutor
license: MIT
metadata:
  hermes:
    tags: [noc, dashboard, provedor, pppoe, radius, wireless, ap, dns, meta, diagnostico, telecom]
    related_skills: [atendimento-isp-n1-n2, sgp-api-integration-ops, mikrotik-ops, ubiquiti-airmax-ops, mimosa-wireless-ops, zabbix-ops]
    safety: read-only, no-customer-passwords, no-production-changes
---

# Dashboard NOC — Diagnóstico por Cliente

## Visão geral

Use esta skill quando o técnico informa o **login PPPoE** do cliente em uma dashboard e o Hermes precisa consultar dados operacionais, correlacionar sinais e gerar uma opinião sobre a saúde da conexão.

O fluxo é **somente leitura**. O técnico usa o painel para acelerar diagnóstico; o Hermes não deve reiniciar equipamento, alterar plano, reprovisionar ONU/CPE, mudar VLAN ou executar comandos destrutivos.

## Fluxo de diagnóstico

```text
Técnico informa login PPPoE
  -> pppoe_lookup(login)
  -> pppoe_disconnect_logs(login)
  -> ap_client_signal(login/mac)
  -> ap_port_health(login/ap_id/interface)
  -> dns_latency_test(domains/resolvers)
  -> http_latency_test(urls)
  -> customer_connection_diagnostic(login)
  -> relatório técnico com opinião
```

## Artefatos publicados

- Skill: `.hermes/skills/forumtelecom/dashboard-noc-diagnostico-cliente/SKILL.md`
- Plugin de referência: `.hermes/skills/forumtelecom/dashboard-noc-diagnostico-cliente/references/noc_customer_diagnostics_plugin.py`
- HTML da dashboard: `docs/dashboard-noc-diagnostico-cliente.html`

## Ferramentas criadas

O plugin de referência fica em `references/noc_customer_diagnostics_plugin.py` e registra estas tools no toolset `noc_customer_diagnostics`:

- `pppoe_lookup(login)` — status PPPoE, IP, uptime, NAS/BNG.
- `pppoe_disconnect_logs(login, hours)` — últimas quedas e motivos de desconexão.
- `ap_client_signal(login, mac)` — sinal, CCQ, ruído e dados RF do cliente no AP.
- `ap_port_health(login|ap_id, interface)` — porta/cabo do AP: link, negociação, CRC/erros, flaps.
- `dns_latency_test(domains, resolvers)` — tempo de resolução DNS.
- `http_latency_test(urls)` — latência HTTP/HTTPS para redes sociais/META ou outros destinos.
- `customer_connection_diagnostic(login)` — orquestra tudo e gera laudo consolidado.

## Instalação do plugin no Hermes

No perfil do Hermes que roda a dashboard/NOC:

```bash
mkdir -p ~/.hermes/plugins/noc_customer_diagnostics
cp references/noc_customer_diagnostics_plugin.py ~/.hermes/plugins/noc_customer_diagnostics/__init__.py
cp templates/noc_customer_diagnostics_plugin.yaml ~/.hermes/plugins/noc_customer_diagnostics/plugin.yaml
```

Ativar plugin e toolset:

```bash
hermes plugins enable noc_customer_diagnostics
hermes tools enable noc_customer_diagnostics
hermes gateway restart
```

Se estiver usando profile específico:

```bash
hermes -p atendimento-isp plugins enable noc_customer_diagnostics
hermes -p atendimento-isp tools enable noc_customer_diagnostics
hermes -p atendimento-isp gateway restart
```

## Variáveis de ambiente

Guardar no `.env` do perfil, nunca no grupo:

```bash
NOC_DIAG_API_BASE_URL="https://noc-api.exemplo.local"
NOC_DIAG_API_TOKEN="token-no-cofre"
NOC_DIAG_TIMEOUT="15"
NOC_DIAG_READ_ONLY="true"
```

Endpoints padrão esperados na API interna:

```text
POST /pppoe/lookup
POST /pppoe/disconnect-logs
POST /ap/client-signal
POST /ap/port-health
```

Cada endpoint deve receber JSON com `login` e `read_only=true`. O token vai no header:

```text
Authorization: Bearer <NOC_DIAG_API_TOKEN>
```

## Contrato de resposta recomendado

### `/pppoe/lookup`

```json
{
  "online": true,
  "ip": "100.64.10.20",
  "uptime": "3h21m",
  "nas": "bng-01",
  "profile": "600M",
  "caller_id": "AA:BB:CC:DD:EE:FF"
}
```

### `/pppoe/disconnect-logs`

```json
{
  "events": [
    {"time": "2026-07-08T10:11:00", "reason": "lost-carrier"},
    {"time": "2026-07-08T07:04:00", "reason": "user-request"}
  ]
}
```

### `/ap/client-signal`

```json
{
  "ap": "Rural-01",
  "client_mac": "AA:BB:CC:DD:EE:FF",
  "signal_dbm": -63,
  "ccq": 91,
  "noise_floor_dbm": -92,
  "tx_rate": "144 Mbps",
  "rx_rate": "144 Mbps"
}
```

### `/ap/port-health`

```json
{
  "ap": "Rural-01",
  "interface": "ether1",
  "link": "up",
  "speed": "1Gbps",
  "duplex": "full",
  "crc_errors": 0,
  "flaps_24h": 0
}
```

## Domínios padrão para META

DNS:

```text
facebook.com
instagram.com
whatsapp.com
messenger.com
```

HTTP:

```text
https://www.facebook.com/
https://www.instagram.com/
https://www.whatsapp.com/
https://www.messenger.com/
```

## Interpretação operacional

- PPPoE offline + ONU/AP sem cliente: investigar físico/autenticação.
- PPPoE online + sinal bom + DNS/HTTP bom: conexão provavelmente saudável.
- PPPoE online + sinal ruim/CCQ baixo: provável última milha/RF/visada/interferência.
- PPPoE online + porta AP com CRC/flap: provável cabo, conector, PoE ou negociação.
- DNS lento/falhando com link saudável: verificar recursivos do provedor.
- META lento/falhando com DNS bom: verificar rota, CDN, CGNAT, IPv6, peering/trânsito.

## Relatório padrão

```text
Login: <mascarado>
Status geral: saudável / atenção / ruim / incompleto
PPPoE: online/offline, IP, uptime, BNG/NAS
Desconexões: resumo dos últimos eventos
AP/RF: sinal, CCQ, ruído, taxa
Porta/cabo AP: link, velocidade, CRC, flaps
DNS: tempo por domínio/resolver
HTTP/META: status e latência por URL
Opinião Hermes: <causa provável>
Próximo passo: <ação sugerida>
```

## Segurança

- Não pedir senha PPPoE, senha Wi-Fi ou credenciais do cliente.
- Não expor IPs/endereços/logins completos em grupo público.
- Não executar alteração de configuração neste fluxo.
- Toda API interna deve usar usuário/token de leitura.
- Registrar auditoria: técnico, login consultado, endpoints chamados e horário.

## Validação

Teste mínimo sem API interna configurada:

```bash
hermes chat -t noc_customer_diagnostics -q 'Use dns_latency_test para facebook.com usando 1.1.1.1 e depois http_latency_test para https://www.facebook.com/'
```

Teste completo quando a API interna estiver pronta:

```bash
hermes chat -t noc_customer_diagnostics -q 'Execute customer_connection_diagnostic para o login cliente.teste e gere relatório curto.'
```

O resultado deve vir como `incompleto` quando a API interna não estiver configurada, e só deve classificar como saudável/atenção/ruim quando PPPoE/AP/porta/DNS/HTTP tiverem dados suficientes.
