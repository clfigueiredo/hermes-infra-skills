# NOC Customer Diagnostics

Plugin Hermes read-only para dashboard de diagnóstico por cliente.

## Ferramentas

- `pppoe_lookup(login)` — status PPPoE, IP, uptime, NAS/BNG.
- `pppoe_disconnect_logs(login, hours)` — histórico de quedas/desconexões.
- `ap_client_signal(login, mac)` — sinal, CCQ, ruído e dados RF do cliente no AP.
- `ap_port_health(login|ap_id, interface)` — link, negociação, CRC/erros e flaps da porta/cabo do AP.
- `dns_latency_test(domains, resolvers)` — tempo de resolução DNS.
- `http_latency_test(urls)` — latência HTTP/HTTPS.
- `customer_connection_diagnostic(login)` — orquestra tudo e gera opinião consolidada.

## Variáveis

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

Todos recebem JSON com `login` e `read_only=true`. O token vai no header `Authorization: Bearer ...`.

Se `NOC_DIAG_API_BASE_URL` não estiver configurado, as ferramentas de equipamento retornam `not_configured`, mas DNS/HTTP continuam funcionando.

## Segurança

- Não coleta nem aceita senha PPPoE.
- Não executa alteração em equipamento.
- Não reinicia, reseta, reprovisiona ou altera VLAN/profile.
- Masca login no relatório consolidado.
