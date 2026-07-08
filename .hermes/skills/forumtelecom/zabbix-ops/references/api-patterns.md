# Zabbix API — Patterns úteis

## Template wrapper (helper bash function)

```bash
#!/bin/bash
zbx_api() {
  local method="$1"
  local params="$2"
  curl -sS -X POST \
    -H "Content-Type: application/json-rpc" \
    -H "Authorization: Bearer $ZABBIX_TOKEN" \
    "$ZABBIX_URL" -d "{
      \"jsonrpc\": \"2.0\",
      \"method\": \"$method\",
      \"params\": $params,
      \"id\": 1
    }"
}

# Uso:
zbx_api "host.get" '{"output": ["host"], "limit": 5}' | jq '.result'
```

## Pattern 1: Top hosts por CPU agora

```bash
zbx_api "history.get" '{
  "output": "extend",
  "history": 0,
  "itemids": [],
  "time_from": '$(($(date +%s) - 300))',
  "sortfield": "clock",
  "sortorder": "DESC",
  "limit": 10
}'
```

Mais útil — query de items de CPU:
```bash
zbx_api "item.get" '{
  "output": ["itemid", "name", "lastvalue", "hostid"],
  "selectHosts": ["host"],
  "search": {"key_": "system.cpu.util"},
  "sortfield": "lastvalue",
  "sortorder": "DESC",
  "limit": 10
}' | jq '.result[] | {host: .hosts[0].host, cpu: .lastvalue}'
```

## Pattern 2: Listar todos os hosts com problema NOW

```bash
zbx_api "problem.get" '{
  "output": ["eventid", "name", "severity", "clock"],
  "selectHosts": ["host"],
  "recent": false,
  "sortfield": "clock",
  "sortorder": "DESC"
}' | jq '.result[] | {host: .hosts[0].host, problem: .name, severity: .severity, age_seconds: (now - (.clock | tonumber))}'
```

## Pattern 3: Forçar coleta imediata de host

Útil quando você acabou de configurar e não quer esperar o ciclo:
```bash
zbx_api "task.create" '{
  "type": 6,
  "request": {"itemid": "<itemid>"}
}'
```

`type: 6` = check now.

## Pattern 4: Bulk acknowledge problemas similares

```bash
# 1. pegar todos os events com mesma name
EVENTS=$(zbx_api "problem.get" '{
  "output": ["eventid"],
  "search": {"name": "Disk space is critically low"}
}' | jq -r '.result[].eventid' | jq -s .)

# 2. ack todos de uma vez
zbx_api "event.acknowledge" '{
  "eventids": '$EVENTS',
  "action": 6,
  "message": "Bulk ack — investigando"
}'
```

## Pattern 5: Maintenance window programada

```bash
# Maintenance todo domingo das 02:00 às 04:00 UTC
zbx_api "maintenance.create" '{
  "name": "Janela manutenção semanal",
  "active_since": '$(date +%s)',
  "active_till": '$(date -d "+1 year" +%s)',
  "hosts": [{"hostid": "<host_id>"}],
  "timeperiods": [{
    "timeperiod_type": 3,
    "every": 1,
    "dayofweek": 1,
    "start_time": 7200,
    "period": 7200
  }]
}'
```

`timeperiod_type`:
- `0` — once
- `2` — daily
- `3` — weekly (`dayofweek` bitmask: 1=Monday, 2=Tuesday, 4=Wed, ...)
- `4` — monthly

## Pattern 6: Discovery rules — adicionar prefix em itens descobertos

Útil pra interfaces de roteador que aparecem dinamicamente:
```bash
zbx_api "discoveryrule.get" '{
  "output": "extend",
  "hostids": "<host_id>",
  "selectItemPrototypes": "extend"
}'
```

## Pattern 7: Backup de template em XML (export)

```bash
zbx_api "configuration.export" '{
  "format": "xml",
  "options": {"templates": ["<template_id>"]}
}' | jq -r '.result' > template-backup.xml
```

Restore:
```bash
zbx_api "configuration.import" '{
  "format": "xml",
  "rules": {
    "templates": {"createMissing": true, "updateExisting": true},
    "items": {"createMissing": true, "updateExisting": true},
    "triggers": {"createMissing": true, "updateExisting": true}
  },
  "source": "'"$(cat template-backup.xml | jq -Rs)"'"
}'
```

## Pattern 8: Métricas para dashboards customizados (via histórico)

```bash
# Tráfego in da eth0 do host X nos últimos 30 minutos
zbx_api "history.get" '{
  "output": "extend",
  "history": 3,
  "itemids": ["<itemid_da_metric>"],
  "time_from": '$(($(date +%s) - 1800))',
  "sortfield": "clock",
  "sortorder": "ASC"
}' | jq '.result[] | {time: .clock, value: .value}'
```

`history` value type:
- `0` — Numeric float
- `1` — Character (string curta)
- `2` — Log
- `3` — Numeric unsigned (integer)
- `4` — Text (string longa)

## Pattern 9: Buscar item.lastvalue de múltiplos hosts

```bash
zbx_api "item.get" '{
  "output": ["itemid", "name", "lastvalue", "units"],
  "selectHosts": ["host"],
  "filter": {"key_": "icmpping"}
}' | jq '.result[] | {host: .hosts[0].host, ping: .lastvalue}'
```

## Pattern 10: Alertas customizados (action.create)

```bash
zbx_api "action.create" '{
  "name": "Alertas críticos pelo Telegram",
  "eventsource": 0,
  "status": 0,
  "esc_period": "5m",
  "filter": {
    "evaltype": 0,
    "conditions": [
      {"conditiontype": 4, "operator": 5, "value": "4"}
    ]
  },
  "operations": [{
    "operationtype": 0,
    "esc_period": 0,
    "esc_step_from": 1,
    "esc_step_to": 1,
    "opmessage_grp": [{"usrgrpid": "<grupo_id>"}],
    "opmessage": {
      "default_msg": 1,
      "mediatypeid": "<telegram_media_id>"
    }
  }]
}'
```

`conditiontype: 4` = trigger severity. `operator: 5` = greater than or equal. `value: 4` = High.
