# RouterOS v6 vs v7 — Diferenças críticas

Carregue este arquivo quando o usuário mencionar versão, ou quando comando falhar.

## Identificar versão
```rsc
:put [/system resource get version]
```

## Tabela

| Domínio | RouterOS 6 | RouterOS 7 |
|---|---|---|
| BGP — peer | `/routing bgp peer print` | `/routing/bgp/connection print` |
| BGP — sessão | (peer status) | `/routing/bgp/session print` |
| BGP — template | embedded em `peer` | `/routing/bgp/template print` |
| BGP — filtros | `/routing filter print` | `/routing/filter/rule print` |
| OSPF — instância | `/routing ospf instance` | `/routing/ospf/instance` |
| OSPF — área | `/routing ospf area` | `/routing/ospf/area` |
| NTP cliente | `/system ntp client print` | `/system/ntp/client print` |
| IPv6 | package separado | nativo |
| WireGuard | não existe | `/interface wireguard` |
| Container | não existe | `/container` (>= 7.4) |
| ROSE storage | não existe | `/disk` |
| ZeroTier | community | `/interface zerotier` (>= 7.10) |
| Bridge VLAN filtering | port-by-port | `/interface bridge vlan` (centralizado) |
| Routing tables | `routing-mark` direto | `/routing/table` declarada antes |

## Mudanças silenciosas (mesmo comando, comportamento diferente)

### `/ip firewall fasttrack-connection`
- v6: dispara em new+est
- v7: requer `connection-state=established,related` explícito

### `/queue tree` com PCQ
- v7: pcq classifier mudou — testar antes de migrar

### `/ip dns`
- v7: introduziu DoH (`use-doh-server`). v6 não tem.

### `/system scheduler`
- v7: aceita expressões cron-style
- v6: só `interval=` e `start-time=`

## Erros comuns ao migrar v6 → v7

1. BGP peer config v6 não funciona em v7 — recriar com `connection` + `template`
2. Routing marks: v6 cria mark em mangle e usa direto. v7 exige declarar tabela em `/routing/table` primeiro
3. OSPF redistribute mudou de lugar
4. Bridge VLAN filtering: migração parcial quebra
