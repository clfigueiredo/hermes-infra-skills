---
name: zabbix-ops
description: Senior Zabbix engineer for monitoring infrastructure (network devices, servers, containers) and creating templates programmatically while respecting API rate limits. Use when the user asks to query, configure, or troubleshoot Zabbix hosts, items, triggers, templates, problems, or maintenance windows; or to create/import templates in bulk respecting PHP-FPM and Postgres lock limits. Triggers include Zabbix, "zabbix api", "zabbix trigger", "zabbix template", "zabbix host", "zabbix problem", "zabbix maintenance", "zabbix snmp", "host está em problema", "criar template Zabbix", "criar template em massa", "import template Zabbix", "rate limit zabbix", "template.massadd", "configuration.import", Zabbix 6.x, Zabbix 7.x.
metadata: { "openclaw": { "emoji": "📊", "requires": { "anyBins": ["curl", "jq"], "env": ["ZABBIX_URL", "ZABBIX_TOKEN"] } } }
---

# Zabbix Operations

Senior monitoring engineer for Zabbix 6.x and 7.x. Speak Brazilian Portuguese, interact via JSON-RPC API.

## Platform context

Zabbix tem 3 superfícies:
- **Frontend (PHP web UI)**: configuração e visualização
- **API JSON-RPC**: automação programática (porta 80/443 + `/api_jsonrpc.php`)
- **Server**: processo `zabbix_server` que coleta dados

Skill atua via **API** (mais robusto pra automação) ou **CLI** (`zabbix_get`, `zabbix_sender`).

## Mandatory workflow

### 1. Authenticate (token preferido sobre login/senha)

Em Zabbix 5.4+ você pode criar API tokens em **Administration > API tokens**.

```bash
ZABBIX_URL="https://zabbix.example.com/api_jsonrpc.php"
ZABBIX_TOKEN="<token-aqui>"

# Test
curl -s -X POST -H "Content-Type: application/json-rpc" "$ZABBIX_URL" -d '{
  "jsonrpc": "2.0",
  "method": "user.checkAuthentication",
  "params": {"sessionid": "'$ZABBIX_TOKEN'"},
  "id": 1
}'
```

### 2. Read before write

Sempre query antes de mutar — entenda o estado atual.

### 3. Apply with caution

Mudanças em template afetam todos os hosts vinculados. Mudanças em trigger podem suprimir alertas críticos.

### 4. Validate

Após mudança, force atualização do host:
```bash
zabbix_get -s <host_ip> -p 10050 -k system.uptime
```

### 5. Report.

## Connection

| Variable | Default | Purpose |
|---|---|---|
| `ZABBIX_URL` | — | required, ex: `https://zbx/api_jsonrpc.php` |
| `ZABBIX_TOKEN` | — | API token |
| `ZABBIX_USER` / `ZABBIX_PASS` | — | alternativa (login/senha) |

## Critical operations via API

### Query hosts (read)
```bash
curl -s -X POST -H "Content-Type: application/json-rpc" "$ZABBIX_URL" -H "Authorization: Bearer $ZABBIX_TOKEN" -d '{
  "jsonrpc": "2.0",
  "method": "host.get",
  "params": {
    "output": ["hostid", "host", "name", "status"],
    "filter": {"name": "router-01"}
  },
  "id": 1
}' | jq '.result'
```

### Listar problemas ativos
```bash
curl -s -X POST -H "Content-Type: application/json-rpc" "$ZABBIX_URL" -H "Authorization: Bearer $ZABBIX_TOKEN" -d '{
  "jsonrpc": "2.0",
  "method": "problem.get",
  "params": {
    "output": "extend",
    "selectAcknowledges": "extend",
    "recent": false,
    "sortfield": ["eventid"],
    "sortorder": "DESC",
    "limit": 50
  },
  "id": 1
}' | jq '.result[] | {name, severity, clock, host: .hosts[0].name}'
```

Severities:
- `0` — Not classified
- `1` — Information
- `2` — Warning
- `3` — Average
- `4` — High
- `5` — Disaster

### Acknowledge problem
```bash
curl -s -X POST -H "Content-Type: application/json-rpc" "$ZABBIX_URL" -H "Authorization: Bearer $ZABBIX_TOKEN" -d '{
  "jsonrpc": "2.0",
  "method": "event.acknowledge",
  "params": {
    "eventids": "<event_id>",
    "action": 6,
    "message": "Acked via API"
  },
  "id": 1
}'
```

Action bitmask:
- `1` — Close
- `2` — Acknowledge
- `4` — Add message
- `8` — Change severity
- `16` — Unacknowledge
- `32` — Suppress
- `64` — Unsuppress
- `128` — Change rank

`6 = 2+4` = ack + add message.

### Criar host
```bash
curl -s -X POST -H "Content-Type: application/json-rpc" "$ZABBIX_URL" -H "Authorization: Bearer $ZABBIX_TOKEN" -d '{
  "jsonrpc": "2.0",
  "method": "host.create",
  "params": {
    "host": "router-novo",
    "name": "Roteador Novo Cliente X",
    "interfaces": [{
      "type": 2, "main": 1, "useip": 1,
      "ip": "10.0.0.1", "dns": "", "port": "161",
      "details": {"version": 2, "community": "{$SNMP_COMMUNITY}"}
    }],
    "groups": [{"groupid": "<group_id>"}],
    "templates": [{"templateid": "<template_id>"}],
    "macros": [{"macro": "{$SNMP_COMMUNITY}", "value": "public"}]
  },
  "id": 1
}'
```

Tipo de interface:
- `1` — Agent (Zabbix agent passivo)
- `2` — SNMP
- `3` — IPMI
- `4` — JMX

### Maintenance window (silenciar alertas)
```bash
NOW=$(date +%s)
END=$(($NOW + 3600))   # 1 hora

curl -s -X POST -H "Content-Type: application/json-rpc" "$ZABBIX_URL" -H "Authorization: Bearer $ZABBIX_TOKEN" -d '{
  "jsonrpc": "2.0",
  "method": "maintenance.create",
  "params": {
    "name": "Manutenção emergencial",
    "active_since": '$NOW',
    "active_till": '$END',
    "hosts": [{"hostid": "<host_id>"}],
    "timeperiods": [{
      "timeperiod_type": 0,
      "start_date": '$NOW',
      "period": 3600
    }]
  },
  "id": 1
}'
```

### Trigger atual de host
```bash
curl -s -X POST -H "Content-Type: application/json-rpc" "$ZABBIX_URL" -H "Authorization: Bearer $ZABBIX_TOKEN" -d '{
  "jsonrpc": "2.0",
  "method": "trigger.get",
  "params": {
    "hostids": "<host_id>",
    "output": ["triggerid", "description", "priority", "status", "value"],
    "filter": {"value": 1},
    "selectLastEvent": "extend"
  },
  "id": 1
}' | jq '.result'
```

`value: 1` = trigger em estado problem (alerta ativo).

## CLI tools

```bash
# Coletar item via agente passivo (test)
zabbix_get -s <host_ip> -p 10050 -k system.uptime
zabbix_get -s <host_ip> -k 'net.if.in[eth0,bytes]'

# Enviar valor via trapper (sender)
zabbix_sender -z <zabbix_server> -s "<host_name>" -k <item_key> -o <value>
```

## Templates comuns no Brasil

- **Network Devices SNMP** (built-in): MikroTik, Cisco, Huawei, Juniper
- **Linux by Zabbix agent / agent2**: server monitoring básico
- **Docker by Zabbix agent2**: containers
- **PostgreSQL/MySQL by Zabbix agent2**: DB
- **HTTP service**: web checks

Para MikroTik especificamente, o template oficial cobre:
- CPU, RAM, uptime
- Interfaces (tráfego, erros, drops)
- Voltagem, temperatura (em CCR/CRS)
- Conexões ativas (firewall connections)

For deeper API patterns see `references/api-patterns.md`.
For template creation respecting rate limits see `references/template-creation-rate-limit.md`.
For a fresh Zabbix + Grafana LXC build on Proxmox, see `proxmox-ops` reference `references/fresh-zabbix-grafana-lxc.md`.

## Fresh LXC install notes

When installing Zabbix Server + frontend from Debian packages in a fresh LXC:

- Import PostgreSQL schema only if the `zabbix` DB is empty; otherwise re-running `server.sql.gz` is destructive/noisy.
- For the frontend to skip the setup wizard, create `/etc/zabbix/web/zabbix.conf.php` with `POSTGRESQL`, DB credentials, `localhost:10051`, and a server name; `/usr/share/zabbix/conf/zabbix.conf.php` is usually a symlink to it.
- With the packaged Nginx config, remove `/etc/nginx/sites-enabled/default` if it shadows the Zabbix vhost on port 80.
- On Zabbix 7.0, changing the built-in `Admin` password through `user.update` requires `current_passwd`; do not assume `passwd` alone works.
- For Grafana installed from Debian packages, reset admin passwords against the same DB/path the service uses: include `--config /etc/grafana/grafana.ini` and `--configOverrides 'cfg:default.paths.data=/var/lib/grafana cfg:default.paths.logs=/var/log/grafana cfg:default.paths.plugins=/var/lib/grafana/plugins cfg:default.paths.provisioning=/etc/grafana/provisioning'`. Plain `grafana-cli --homepath /usr/share/grafana admin reset-admin-password` can update `/usr/share/grafana/data/grafana.db` while the service authenticates against `/var/lib/grafana/grafana.db`.
- If Grafana rejects a known-good password after many attempts, clear lockout state (`login_attempt`) and restart Grafana before re-testing; verify with `/api/user` or the `/login` form, not only `/api/health`.
- When creating the Grafana Zabbix datasource for `alexanderzobnin-zabbix-datasource` 6.4.x via API, set `jsonData.timeout` as a numeric string such as `"30"`, not `"30s"`; `"30s"` makes plugin health/query fail with `failed to parse timeout: strconv.Atoi: parsing "30s": invalid syntax`. Validate with `/api/datasources/uid/<uid>/health` and a real `/api/ds/query` before creating dashboards.

For LAN onboarding/discovery workflow, see `references/network-scan-to-zabbix-onboarding.md`.
For building a lightweight custom MikroTik SNMP template (CPU, interface in/out, uptime only), see `references/custom-mikrotik-minimal-snmp-template.md`.

## Safety rules

### NEVER without confirmation
- `host.delete` (apaga host e todo histórico)
- `template.delete` (afeta todos os hosts vinculados)
- Mass `trigger.update status=disabled` (silencia alertas críticos)
- `housekeeping.delete` (apaga histórico)

### ALWAYS warn before
- Mudança em template usado em produção
- Maintenance window que cobre múltiplos hosts críticos
- Mudança em macro global
- Disable trigger em horário comercial

### Confirmation pattern
> Operação perigosa: `<comando>`
> Impacto: <hosts/triggers afetados>
> Para executar, responda: `CONFIRMO <comando>`

## Casos típicos de provedor (deep)

### Arquitetura padrão de Zabbix em provedor

- **Zabbix Server** central + **Postgres com TimescaleDB** (compressão de history/trends, ~70% economia de disco)
- **Zabbix Proxies distribuídos**: um por POP/datacenter, coleta local e envia ao server
- **Auto-discovery** via Network Discovery (range de IPs) ou LLD em template
- **Notificação**: webhook → Evolution API (WhatsApp) e Telegram nativo
- **Housekeeping** agressivo: history 7-30 dias, trends 365 dias

Sem proxy distribuído, provedor com 5k+ hosts vira gargalo — proxy reduz latência de polling e isola falhas de rede.

### Discovery automático de equipamentos novos

Padrão: range de IP gerência da rede → discovery rule → auto-add com template baseado em SNMP sysObjectID.

```bash
# Criar discovery rule via API
curl -s -X POST -H "Content-Type: application/json-rpc" "$ZABBIX_URL" \
  -H "Authorization: Bearer $ZABBIX_TOKEN" -d '{
  "jsonrpc": "2.0",
  "method": "drule.create",
  "params": {
    "name": "Rede gerência ISP",
    "iprange": "10.0.0.1-254",
    "delay": "1h",
    "dchecks": [{
      "type": 11,
      "snmp_community": "{$SNMP_COMMUNITY}",
      "key_": "sysObjectID.0",
      "ports": "161",
      "uniq": 1
    }]
  }, "id": 1}'
```

Combine com **action de auto-add** (configuration > actions > discovery actions) que vincula template baseado no OID retornado.

### Webhook → Evolution API (WhatsApp)

Mediatype tipo Webhook em Administration > Media types:

```javascript
// Script JS do mediatype
try {
    var params = JSON.parse(value);
    var req = new HttpRequest();
    req.addHeader('Content-Type: application/json');
    req.addHeader('apikey: ' + params.evolution_apikey);
    var payload = JSON.stringify({
        number: params.sendTo,
        text: params.subject + '\n\n' + params.message
    });
    var resp = req.post(
        params.evolution_url + '/message/sendText/' + params.instance,
        payload
    );
    if (req.getStatus() !== 201) throw 'Status ' + req.getStatus();
    return 'OK';
} catch (err) {
    Zabbix.log(4, '[Evolution Webhook] ' + err);
    throw err;
}
```

User parameters do mediatype: `evolution_url`, `evolution_apikey`, `instance`, `sendTo`, `subject`, `message`.

### Operações típicas via WhatsApp (NetAgent)

| Pedido | Ação |
|---|---|
| "Quem tá com problema agora?" | `problem.get` ordenado por severity |
| "Adicionar router-X no Zabbix" | `host.create` com template SNMP + macros |
| "Silenciar alerta da OLT durante manutenção" | `maintenance.create` 2h |
| "Tráfego do uplink no último dia" | `history.get` do item bytes_in/out + cálculo |
| "Desabilitar host inativo" | `host.update` status=1 |

---

## Criação de templates respeitando rate limit da API

**Tema crítico**: a API JSON-RPC do Zabbix não tem rate limit hardcoded, mas **na prática quebra** em três pontos: (1) PHP-FPM com workers limitados, (2) max_input_vars do PHP, (3) bloqueio de tabela no Postgres durante `template.massadd` ou criação em massa de itens.

Provedor que tenta criar template com 200 itens via 200 chamadas paralelas derruba o frontend.

### Limites práticos a respeitar

| Operação | Limite recomendado |
|---|---|
| Requests paralelos | **5 simultâneos** (PHP-FPM default = 5 workers) |
| Items por `item.create` em batch | **50 por chamada** |
| Triggers por `trigger.create` em batch | **30 por chamada** |
| Hosts por `host.create` em batch | **20 por chamada** |
| Pausa entre lotes | **200ms** mínimo |
| Tamanho máx do JSON | `max_input_vars=10000`, `post_max_size=16M` |

Se você precisa criar template grande (300+ items), faça **batches sequenciais** com pausa entre eles.

### Pattern: batch sequencial com retry exponencial

```bash
#!/bin/bash
# create-template-with-rate-limit.sh

ZBX_API="${ZABBIX_URL:-https://zabbix.example.com/api_jsonrpc.php}"
ZBX_TOKEN="${ZABBIX_TOKEN}"

zbx_call() {
  local method="$1"
  local params="$2"
  local attempt=0
  local max_attempts=5
  local delay=1

  while [ $attempt -lt $max_attempts ]; do
    response=$(curl -s -X POST \
      -H "Content-Type: application/json-rpc" \
      -H "Authorization: Bearer $ZBX_TOKEN" \
      "$ZBX_API" -d "{
        \"jsonrpc\": \"2.0\",
        \"method\": \"$method\",
        \"params\": $params,
        \"id\": 1
      }")

    if echo "$response" | jq -e '.error' > /dev/null 2>&1; then
      err_code=$(echo "$response" | jq -r '.error.code')
      # -32500 = application error (lock, busy)
      if [ "$err_code" = "-32500" ] || [ "$err_code" = "-32603" ]; then
        attempt=$((attempt + 1))
        sleep $delay
        delay=$((delay * 2))
        continue
      fi
      echo "$response" >&2
      return 1
    fi
    echo "$response"
    return 0
  done
  echo "Max retries exceeded for $method" >&2
  return 1
}

# Throttling helper
throttle() { sleep 0.2; }
```

### Workflow completo: criar template + 200 items + 50 triggers

```bash
# 1. Criar template (1 chamada)
TEMPLATE_RESP=$(zbx_call "template.create" '{
  "host": "Template MikroTik Custom ISP",
  "name": "Template MikroTik Custom ISP",
  "groups": [{"groupid": "1"}],
  "macros": [
    {"macro": "{$SNMP_COMMUNITY}", "value": "public"},
    {"macro": "{$IF.UTIL.MAX}", "value": "90"}
  ]
}')
TEMPLATE_ID=$(echo "$TEMPLATE_RESP" | jq -r '.result.templateids[0]')
throttle

# 2. Criar items em batches de 50
ITEMS_JSON=$(cat items.json)   # array de 200 items
TOTAL=$(echo "$ITEMS_JSON" | jq 'length')
BATCH_SIZE=50
BATCHES=$(( (TOTAL + BATCH_SIZE - 1) / BATCH_SIZE ))

for i in $(seq 0 $((BATCHES - 1))); do
  START=$((i * BATCH_SIZE))
  BATCH=$(echo "$ITEMS_JSON" | jq ".[$START:$((START + BATCH_SIZE))] | map(. + {hostid: \"$TEMPLATE_ID\"})")
  zbx_call "item.create" "$BATCH" > /dev/null
  echo "✓ Batch items $((i+1))/$BATCHES"
  throttle
done

# 3. Criar triggers em batches de 30 (depois dos items)
TRIGGERS_JSON=$(cat triggers.json)
TOTAL=$(echo "$TRIGGERS_JSON" | jq 'length')
BATCH_SIZE=30
BATCHES=$(( (TOTAL + BATCH_SIZE - 1) / BATCH_SIZE ))

for i in $(seq 0 $((BATCHES - 1))); do
  START=$((i * BATCH_SIZE))
  BATCH=$(echo "$TRIGGERS_JSON" | jq ".[$START:$((START + BATCH_SIZE))]")
  zbx_call "trigger.create" "$BATCH" > /dev/null
  echo "✓ Batch triggers $((i+1))/$BATCHES"
  throttle
done

echo "Template ID: $TEMPLATE_ID"
```

### Mass-update mais eficiente que loop

Para vincular template a 100 hosts existentes — **NÃO** faça loop de `host.update`. Use **`template.massadd`** numa única chamada:

```bash
zbx_call "template.massadd" '{
  "templates": [{"templateid": "10001"}],
  "hosts": [
    {"hostid": "1001"}, {"hostid": "1002"}, {"hostid": "1003"}
    // ... até 500 num único call funciona bem
  ]
}'
```

Esse método é **transacional** — ou tudo entra ou nada. Muito melhor que 100 chamadas individuais.

### Importação via XML/YAML (alternativa quando viável)

Para template grande pré-pronto, importar via API `configuration.import` é **mais rápido** que criar item por item:

```bash
TEMPLATE_XML=$(cat template-mikrotik-custom.xml | base64 -w0)

zbx_call "configuration.import" "{
  \"format\": \"xml\",
  \"rules\": {
    \"templates\": {\"createMissing\": true, \"updateExisting\": true},
    \"items\": {\"createMissing\": true, \"updateExisting\": true},
    \"triggers\": {\"createMissing\": true, \"updateExisting\": true}
  },
  \"source\": \"$(echo "$TEMPLATE_XML" | base64 -d | jq -Rs .)\"
}"
```

Limite prático: arquivo XML <16MB (`post_max_size`). Para templates monstro, dividir em múltiplos arquivos.

### Detecção de erro de overload

Códigos retornados pela API quando rate é alto demais:

| Código | Significado | Ação |
|---|---|---|
| `-32500` | Application error | Retry com backoff (lock de tabela) |
| `-32600` | Invalid request | Erro do client, **não retry** |
| `-32602` | Invalid params | Erro do client, **não retry** |
| `-32603` | Internal error | Retry com backoff (server overload) |
| `-32700` | Parse error | JSON malformado, **não retry** |

HTTP 504 ou timeout do curl = PHP-FPM travou em workers. Reduza paralelismo.

### Operações comuns via NetAgent

| Pedido | Estratégia |
|---|---|
| "Crie template MikroTik com 50 itens" | `template.create` + `item.create` em 1 batch |
| "Crie template Huawei OLT com 300 itens" | template + 6 batches de 50 + throttle |
| "Importe esse XML" | `configuration.import` se <16MB |
| "Vincule template X a 200 hosts" | `template.massadd` numa chamada só |
| "Replicar template entre 2 instâncias Zabbix" | `configuration.export` na origem + `configuration.import` no destino |

## Report template

```markdown
## Operação Zabbix: <título>
**Servidor:** <url>
**Versão:** 6.4 / 7.0

**Query/Mudança:**
```json
<API call ou descrição>
```

**Resultado:** <resumo>
**Próximos passos:** <bullets>
```
