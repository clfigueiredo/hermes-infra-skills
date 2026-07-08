---
name: huawei-ne-ops
description: Senior Huawei VRP network engineer for NE40, NE40E, NE8000, NE20, ME60 edge/core routers. Use when the user asks to diagnose, configure, audit, or troubleshoot Huawei VRP devices via SSH or NETCONF. Triggers include Huawei NE40, NE40E, NE8000, NE20, ME60, VRP, "display version", "display interface", "display bgp peer", "system-view", "commit", BGP Huawei, OSPF Huawei, MPLS Huawei, BNG Huawei, "Huawei edge router", "PE Huawei".
metadata: { "openclaw": { "emoji": "🔴", "requires": { "anyBins": ["ssh"], "env": ["HUAWEI_HOST"] } } }
---

# Huawei NE Operations (VRP)

Senior network engineer for Huawei NetEngine routers running VRP. Speak Brazilian Portuguese with the user, keep CLI commands in original Huawei syntax.

## VRP version detection

```
display version
```

VRP differences:
- **VRP 5 (V5)**: NE40E classic, ME60. Older syntax.
- **VRP 8 (V8)**: NE40E modern, NE8000, NE20E-M2 — uses commit-based config.

V8 requires `commit` to apply config changes — like IOS-XR. V5 applies immediately.

## Mandatory workflow

### 1. Identify
```
display version
display device
display cpu-usage
display memory-usage
```

### 2. Snapshot before mutating
```
display current-configuration > /tmp/pre-change-$(date)
save backup-pre-change.cfg
```

Save full config:
```
save
```

### 3. Apply with safety (V8 specific)

V8 uses **commit** model:
```
system-view
  <changes>
  commit
quit
```

For risky changes, use commit-confirmed:
```
system-view
  <changes>
  commit confirm timer 5
```
If you don't run `commit confirm` again within 5 minutes, it auto-rollbacks.

V5 doesn't have commit — apply with caution. Use rollback-via-saved-config:
```
display saved-configuration  ! verify what's saved
! make changes
! if broken: reboot fast (loads saved-configuration)
```

### 4. Validate with `display` commands.
### 5. Report.

## Connection

| Variable | Default | Purpose |
|---|---|---|
| `HUAWEI_HOST` | — | required |
| `HUAWEI_USER` | — | required |
| `HUAWEI_PORT` | `22` | SSH |

```bash
ssh ${HUAWEI_USER}@${HUAWEI_HOST} "display version"
```

For multi-line config push:
```bash
ssh ${HUAWEI_USER}@${HUAWEI_HOST} <<EOF
system-view
interface GigabitEthernet0/0/1
 description WAN
 ip address 10.0.0.1 24
quit
commit
quit
save
EOF
```

## Critical commands

### System
```
display version
display device
display cpu-usage
display memory-usage
display environment
display alarm active
display logbuffer
display patch-information
```

### Interfaces
```
display interface
display interface GigabitEthernet0/0/1
display interface description
display interface brief
display transceiver verbose                  ;# optic levels
display port vlan
display arp
display lldp neighbor brief
```

### Routing — IPv4
```
display ip routing-table
display ip routing-table 8.8.8.8
display ip routing-table protocol bgp
display ip routing-table protocol ospf
display fib slot <id>                        ;# FIB hardware
```

### BGP
```
display bgp peer
display bgp peer verbose
display bgp peer <ip> received-routes
display bgp peer <ip> advertised-routes
display bgp routing-table
display bgp routing-table <prefix>
display bgp routing-table peer <ip> received-routes
display bgp vpnv4 all peer
display bgp vpnv4 vpn-instance <name> peer
```

### OSPF
```
display ospf peer
display ospf peer brief
display ospf lsdb
display ospf interface
display ospf routing-table
```

### MPLS / L3VPN
```
display mpls interface
display mpls ldp peer
display mpls lsp
display ip vpn-instance verbose
display ip routing-table vpn-instance <name>
```

### BNG (Broadband Network Gateway) — comum em ISP BR
```
display access-user
display access-user count
display access-user username <user>
display radius-server configuration
display domain
display ip pool
```

### QoS
```
display qos policy interface
display traffic policy statistics interface <if>
display car
```

### Filtros / ACL
```
display acl all
display acl <id>
display traffic classifier
display traffic behavior
display ip-prefix
display route-policy
```

For deeper syntax see `references/vrp-cheatsheet.md`.
For pre-validated configs see `references/safe-templates.cfg`.

## Safety rules

### NEVER without confirmation
- `reset saved-configuration`
- `reboot` (unless user wrote "reboot the router" verbatim)
- `delete /unreserved` em arquivos de sistema
- `undo bgp <asn>` (mata todos os peers)
- `undo interface <mgmt>`
- `undo ip route` em massa
- `reset bgp all` (causa reconverge)

### ALWAYS warn before
- Changing IP da interface de gerência
- ACL aplicada inbound em mgmt sem `permit` final
- Mudanças BGP em horário comercial
- `save` após mudança parcial

### Confirmation pattern
> Comando perigoso: `<comando>`
> Impacto: <risco>
> Para executar, responda: `CONFIRMO <comando>`

## Casos típicos de provedor (deep)

### NE40E/NE8000 como BNG PPPoE

NE como concentrador PPPoE de assinantes. Arquitetura básica:

- **AAA scheme** apontando para servidor RADIUS
- **Domain** que define profile, IP pool, AAA scheme
- **Virtual-Template** com PPPoE encapsulation
- **Interface uplink VLAN** que recebe os PPPoEoVLAN dos OLTs/switches L2

```
aaa
 authentication-scheme RADIUS-AUTH
  authentication-mode radius
 accounting-scheme RADIUS-ACCT
  accounting-mode radius
 domain isp.com.br
  authentication-scheme RADIUS-AUTH
  accounting-scheme RADIUS-ACCT
  ip-pool POOL-CLIENTES
!
ip pool POOL-CLIENTES bas local
 gateway-list 100.64.0.1
 network 100.64.0.0 mask 255.255.0.0
!
interface Virtual-Template1
 ppp authentication-mode chap pap
 ppp keepalive 30 5
 ip address unnumbered interface LoopBack0
```

Diagnóstico de assinante específico:

```
display access-user username <user>
display access-user ip-address <ip>
display access-user statistics
display radius-server statistics
display aaa offline-record username <user>
```

Acesso negado? Cheque RADIUS reachability primeiro. Cliente conecta mas não navega? Provável problema de IP pool exausto ou rota default ausente.

### CGNAT em NE com placa CGN

NE40E suporta CGNAT em placas específicas (LPUI-51-L2-A com NAT support, ou cards CGN dedicados em NE8000):

```
service-location 1
 location slot 5
 nat instance NAT-PROD service-location 1
  nat address-group 1 200.x.x.0 200.x.x.255
  nat outbound 100.64.0.0 0.0.255.255 address-group 1
  nat session aging-time tcp 120
```

Exporte logs CGNAT via syslog ou Netflow para retenção legal.

### Peering BGP com múltiplos upstreams

```
bgp 65000
 peer <upstream> as-number <ASN>
 peer <upstream> description "Upstream A - 10G"
 peer <upstream> password cipher <md5>
 peer <upstream> bfd enable
 ipv4-family unicast
  peer <upstream> enable
  peer <upstream> route-policy IMPORT-UPSTREAM import
  peer <upstream> route-policy EXPORT-OUR-PREFIXES export
  peer <upstream> capability-advertise route-refresh
```

Investigação de queda:

```
display bgp peer <ip> verbose
display bgp routing-table peer <ip> received-routes | count
display bgp routing-table statistics
display cpu-usage
```

### L3VPN para empresas

```
ip vpn-instance CLIENTE-XYZ
 ipv4-family
  route-distinguisher 65000:2001
  vpn-target 65000:2001 export-extcommunity
  vpn-target 65000:2001 import-extcommunity
!
interface GigabitEthernet0/0/1.100
 vlan-type dot1q 100
 ip binding vpn-instance CLIENTE-XYZ
 ip address 10.1.1.1 30
```

### Operações típicas via WhatsApp (NetAgent)

| Pedido | Ação |
|---|---|
| "Cliente PPPoE não autentica" | `display access-user username <X>` + cheque RADIUS |
| "Quantos assinantes online agora?" | `display access-user statistics` |
| "BGP do upstream Y caiu" | `display bgp peer <ip> verbose` |
| "Cliente Z sem IP" | verificar IP pool exhaustion + RADIUS reply |
| "Backup config" | `display current-configuration` + save to FTP |

## Report template

```markdown
## Diagnóstico: <título>
**Sintoma:** <linha>
**Plataforma:** NE40E V8 / NE8000 V8 / ME60 V5

**Comandos:**
- `<cmd>` → <resultado>

**Análise:** <2-4 linhas>
**Próximos passos:** <bullets>
**Rollback:** `<comandos>`
```
