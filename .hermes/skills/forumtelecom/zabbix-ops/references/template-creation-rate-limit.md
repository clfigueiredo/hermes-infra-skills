# Zabbix — Criação de templates respeitando rate limit

Referência completa para criar/importar templates em massa via API JSON-RPC sem derrubar o frontend.

## Por que isso importa

A API Zabbix não tem rate limit explícito, mas há **três pontos de saturação** reais:

1. **PHP-FPM workers**: default ~5 workers em frontend pequeno. 10+ requests paralelos = fila.
2. **Postgres locks**: criação massiva de items/triggers segura tabelas (`items`, `functions`, `triggers`).
3. **PHP `max_input_vars`**: default 10000. JSON com array gigante quebra parse.

Em provedor com 5k+ hosts e Zabbix server modesto, importar template grande sem cuidado **trava o frontend** por minutos.

## Limites práticos (testados em produção)

| Operação | Tamanho recomendado por chamada |
|---|---|
| `item.create` | até 50 items |
| `trigger.create` | até 30 triggers |
| `host.create` | até 20 hosts |
| `template.massadd` | até 500 hostids vinculados a 1 template |
| `configuration.import` (XML/YAML) | até 16MB de payload |
| Pausa entre chamadas | 200ms mínimo |
| Paralelismo | 3-5 simultâneos máximo |

## Helper bash robusto

```bash
#!/bin/bash
# zbx-helper.sh — source este arquivo nos seus scripts

ZBX_API="${ZABBIX_URL}"
ZBX_TOKEN="${ZABBIX_TOKEN}"

zbx_call() {
  local method="$1"
  local params="$2"
  local attempt=0
  local max_attempts=5
  local delay=1

  while [ $attempt -lt $max_attempts ]; do
    response=$(curl -sS -X POST \
      --max-time 60 \
      -H "Content-Type: application/json-rpc" \
      -H "Authorization: Bearer $ZBX_TOKEN" \
      "$ZBX_API" -d "{
        \"jsonrpc\": \"2.0\",
        \"method\": \"$method\",
        \"params\": $params,
        \"id\": 1
      }")

    # curl falhou (timeout, conn refused)
    if [ -z "$response" ]; then
      attempt=$((attempt + 1))
      sleep $delay
      delay=$((delay * 2))
      continue
    fi

    # Erro de aplicação — retry para -32500 e -32603
    if echo "$response" | jq -e '.error' > /dev/null 2>&1; then
      err_code=$(echo "$response" | jq -r '.error.code')
      err_msg=$(echo "$response" | jq -r '.error.message + ": " + .error.data')
      case "$err_code" in
        -32500|-32603)
          echo "[retry $attempt] $err_msg" >&2
          attempt=$((attempt + 1))
          sleep $delay
          delay=$((delay * 2))
          continue
          ;;
        *)
          echo "[fatal] $err_msg" >&2
          return 1
          ;;
      esac
    fi

    echo "$response"
    return 0
  done
  echo "[max-retries] $method failed after $max_attempts attempts" >&2
  return 1
}

zbx_throttle() { sleep 0.2; }

zbx_batch() {
  # zbx_batch <method> <items_json_array> <batch_size>
  local method="$1"
  local items_json="$2"
  local batch_size="$3"
  local total=$(echo "$items_json" | jq 'length')
  local batches=$(( (total + batch_size - 1) / batch_size ))
  local i

  for i in $(seq 0 $((batches - 1))); do
    local start=$((i * batch_size))
    local batch=$(echo "$items_json" | jq ".[$start:$((start + batch_size))]")
    zbx_call "$method" "$batch" > /dev/null || return 1
    echo "  ✓ $method batch $((i+1))/$batches" >&2
    zbx_throttle
  done
}
```

## Caso 1: Criar template do zero com 200 items + 50 triggers

```bash
source zbx-helper.sh

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
echo "Template criado: $TEMPLATE_ID"
zbx_throttle

# 2. Items em batches de 50 (com hostid injetado)
ITEMS_WITH_HOST=$(jq --arg tid "$TEMPLATE_ID" 'map(. + {hostid: $tid})' items.json)
zbx_batch "item.create" "$ITEMS_WITH_HOST" 50

# 3. Triggers em batches de 30
zbx_batch "trigger.create" "$(cat triggers.json)" 30

echo "Template completo: $TEMPLATE_ID"
```

Estrutura do `items.json`:

```json
[
  {
    "name": "CPU utilization",
    "key_": "system.cpu.util[,user]",
    "type": 20,
    "value_type": 0,
    "delay": "1m",
    "history": "7d",
    "trends": "365d",
    "units": "%"
  },
  {
    "name": "Free memory",
    "key_": "vm.memory.size[available]",
    "type": 20,
    "value_type": 3,
    "delay": "1m",
    "units": "B"
  }
]
```

`type: 20` = SNMP agent. Outros tipos: `0` = Zabbix agent, `7` = Zabbix agent active, `2` = trapper, `15` = calculated.

## Caso 2: Importar template via XML

Mais rápido que criar item-por-item se o template já existe pronto:

```bash
source zbx-helper.sh

XML_FILE="template-mikrotik-custom.xml"
SIZE_BYTES=$(stat -c%s "$XML_FILE")

if [ $SIZE_BYTES -gt 16777216 ]; then
  echo "ERRO: arquivo > 16MB, dividir em múltiplos templates"
  exit 1
fi

XML_CONTENT=$(jq -Rs . < "$XML_FILE")

zbx_call "configuration.import" "{
  \"format\": \"xml\",
  \"rules\": {
    \"templates\": {\"createMissing\": true, \"updateExisting\": true},
    \"items\": {\"createMissing\": true, \"updateExisting\": true, \"deleteMissing\": false},
    \"triggers\": {\"createMissing\": true, \"updateExisting\": true, \"deleteMissing\": false},
    \"discoveryRules\": {\"createMissing\": true, \"updateExisting\": true},
    \"valueMaps\": {\"createMissing\": true, \"updateExisting\": false},
    \"groups\": {\"createMissing\": true}
  },
  \"source\": $XML_CONTENT
}"
```

Importante: `deleteMissing: false` em items/triggers — senão o import remove tudo que não está no XML, derrubando hosts existentes.

## Caso 3: Vincular template a 200 hosts existentes

**Errado** (loop):
```bash
# NÃO FAZER ISSO — 200 chamadas sequenciais demora minutos
for hostid in $(cat hostids.txt); do
  zbx_call "host.update" "{\"hostid\": \"$hostid\", \"templates\": [{\"templateid\": \"$TEMPLATE_ID\"}]}"
done
```

**Certo** (transacional):
```bash
HOSTS_JSON=$(jq -R '.' < hostids.txt | jq -s 'map({hostid: .})')

zbx_call "template.massadd" "{
  \"templates\": [{\"templateid\": \"$TEMPLATE_ID\"}],
  \"hosts\": $HOSTS_JSON
}"
```

`template.massadd` aceita até ~500 hostids num call. Acima disso, dividir.

## Caso 4: Replicar template entre instâncias Zabbix

Padrão: export de origem + import no destino.

```bash
# Origem
ZBX_API="$SOURCE_URL" ZBX_TOKEN="$SOURCE_TOKEN" \
  zbx_call "configuration.export" '{
    "options": {"templates": ["10001"]},
    "format": "yaml"
  }' | jq -r '.result' > template-export.yaml

# Destino
TEMPLATE_YAML=$(jq -Rs . < template-export.yaml)
ZBX_API="$DEST_URL" ZBX_TOKEN="$DEST_TOKEN" \
  zbx_call "configuration.import" "{
    \"format\": \"yaml\",
    \"rules\": {
      \"templates\": {\"createMissing\": true, \"updateExisting\": true},
      \"items\": {\"createMissing\": true, \"updateExisting\": true},
      \"triggers\": {\"createMissing\": true, \"updateExisting\": true},
      \"groups\": {\"createMissing\": true}
    },
    \"source\": $TEMPLATE_YAML
  }"
```

## Códigos de erro JSON-RPC

| Código | Significado | Retry? |
|---|---|---|
| `-32500` | Application error (lock, busy) | **SIM** com backoff |
| `-32600` | Invalid request | NÃO |
| `-32602` | Invalid params | NÃO |
| `-32603` | Internal error (overload) | **SIM** com backoff |
| `-32700` | Parse error (JSON inválido) | NÃO |

HTTP-level:
- **504 Gateway Timeout** = PHP-FPM cheio. Reduza paralelismo.
- **502 Bad Gateway** = nginx não conseguiu falar com PHP. Idem.
- **413 Payload Too Large** = `client_max_body_size` ou `post_max_size` baixo.

## Tunings recomendados no servidor Zabbix

Para frontend que recebe imports grandes, ajustar:

```ini
; /etc/php/8.x/fpm/php.ini
post_max_size = 32M
upload_max_filesize = 32M
max_input_vars = 20000
max_execution_time = 300
memory_limit = 512M
```

```nginx
# nginx site config
client_max_body_size 32M;
fastcgi_read_timeout 300s;
```

```ini
; PHP-FPM pool
pm.max_children = 20
pm.start_servers = 5
pm.min_spare_servers = 3
pm.max_spare_servers = 10
```

Sem isso, frontend default não aguenta nem template médio (~5MB XML).

## Observabilidade do próprio import

Logar tempo, retries, falhas:

```bash
zbx_call_logged() {
  local start=$(date +%s%3N)
  local result=$(zbx_call "$@")
  local end=$(date +%s%3N)
  local duration=$((end - start))
  echo "[$duration ms] $1" >&2
  echo "$result"
}
```

Em scripts de produção, **sempre** loggar para ter histórico de quando começou a saturar.
