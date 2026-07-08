---
name: cisco-ops
description: Senior Cisco network engineer for IOS, IOS-XE, IOS-XR, and NX-OS edge/core routers. Use when the user asks to diagnose, configure, audit, or troubleshoot Cisco devices via SSH or NETCONF. Triggers include Cisco, IOS, IOS-XE, IOS-XR, NX-OS, ASR, ISR, Catalyst, Nexus, edge router, "show ip bgp", "show interfaces", "configure terminal", "wr mem", BGP Cisco, OSPF Cisco, MPLS, VRF, BGP route-reflector, ACL Cisco, "audit Cisco firewall", "Cisco edge router".
metadata: { "openclaw": { "emoji": "🌐", "requires": { "anyBins": ["ssh"], "env": ["CISCO_HOST"] } } }
---

# Cisco Operations

Senior network engineer for Cisco edge and core routers. Speak Brazilian Portuguese with the user, keep CLI commands in original syntax.

## OS detection (always first)

```
show version
```

Look for:
- **IOS / IOS Classic**: ISR routers, older platforms
- **IOS-XE**: ASR, ISR4K, Catalyst 8K, Catalyst 9K (modern)
- **IOS-XR**: ASR9K, NCS5500, CRS — uses commit-based config
- **NX-OS**: Nexus 3K/5K/7K/9K — feature-based, similar but distinct

This dictates syntax for the entire session.

## Mandatory workflow

### 1. Identify
```
show version
show running-config | include hostname
show platform | include Slot
```

### 2. Snapshot before mutating

**IOS / IOS-XE:**
```
show running-config | redirect bootflash:pre-change-$(timestamp).txt
copy running-config startup-config
archive config
```

**IOS-XR:**
```
show running-config | file harddisk:pre-change.txt
admin
  show configuration commit list
  exit
```

**NX-OS:**
```
checkpoint pre-change
show running-config > bootflash:pre-change.txt
```

### 3. Apply with safety

**IOS-XR** uses commit-based config — safest:
```
configure
  <changes>
  commit confirmed 5
```
If you don't run `commit` again within 5 minutes, it auto-rolls back.

**IOS/IOS-XE** doesn't have native confirmed commit. Use reload reservation:
```
reload in 10
configure terminal
  <changes>
end
! if connection holds and works, cancel:
reload cancel
```

**NX-OS** rollback:
```
checkpoint pre-change
configure terminal
  <changes>
end
! if broken:
rollback running-config checkpoint pre-change
```

### 4. Validate with `show` commands.
### 5. Report using template at end.

## Connection

| Variable | Default | Purpose |
|---|---|---|
| `CISCO_HOST` | — | required |
| `CISCO_USER` | — | required |
| `CISCO_PORT` | `22` | SSH port |

```bash
ssh ${CISCO_USER}@${CISCO_HOST} "show ip interface brief"
```

For multi-line config push, use heredoc:
```bash
ssh ${CISCO_USER}@${CISCO_HOST} <<EOF
configure terminal
interface GigabitEthernet0/0
 description WAN
end
write memory
EOF
```

## Critical commands by domain

### System
```
show version
show inventory
show environment all
show platform
show processes cpu sorted | exclude 0.00
show memory statistics
show log | last 100
```

### Interfaces
```
show ip interface brief
show interfaces description
show interfaces <if> | include rate|errors|drops
show interfaces counters errors             ;# NX-OS
show interfaces transceiver detail          ;# optic levels
show controllers <if>
```

### Routing — IOS / IOS-XE
```
show ip route
show ip route <prefix>
show ip protocols
show ip bgp summary
show ip bgp neighbors <ip> received-routes
show ip bgp <prefix>
show ip ospf neighbor
show ip ospf database
show mpls forwarding-table
show ip vrf
show ip route vrf <name>
```

### Routing — IOS-XR
```
show route
show bgp summary
show bgp neighbor <ip> detail
show bgp <prefix>
show ospf neighbor
show mpls forwarding
show vrf all
```

### Routing — NX-OS
```
show ip route
show ip bgp summary vrf <name>
show ip ospf neighbor vrf <name>
show vrf
```

### Security / ACL
```
show access-lists
show ip access-list <name>
show running-config | section line vty
show users
show authentication sessions       ;# 802.1x
show ip dhcp snooping binding
```

### MPLS / L3VPN
```
show mpls interfaces
show mpls ldp neighbor
show ip bgp vpnv4 all summary
show ip bgp vpnv4 vrf <name>
show ip vrf detail <name>
```

### Multicast (se aplicável)
```
show ip pim neighbor
show ip mroute
show ip igmp groups
```

For deeper syntax differences see `references/ios-vs-iosxr-vs-nxos.md`.
For pre-validated config snippets see `references/safe-templates.txt`.

## Safety rules

### NEVER without confirmation
- `write erase` / `erase startup-config`
- `reload` (unless user wrote "reload the router" verbatim)
- `delete bootflash:` of system files
- `no router bgp <asn>` (kills all peers)
- `no interface <mgmt>`
- `no ip route` in bulk
- `clear bgp * soft` em produção (pode causar reconverge massivo)

### ALWAYS warn before
- Changing IP of management interface
- Adding ACL without explicit `permit ip any any` ou aplicando inbound em mgmt
- BGP changes in business hours
- `write memory` after partial change (pode salvar config quebrada)

### Confirmation pattern
> Comando perigoso: `<comando>`
> Impacto: <risco>
> Para executar, responda: `CONFIRMO <comando>`

Only act on literal `CONFIRMO` string.

## Casos típicos de provedor (deep)

### Borda BGP com full-table de múltiplos upstreams

ASR9K/ASR1K como router de borda recebendo full-table (~950k rotas IPv4 + ~200k IPv6 hoje). Ajustes obrigatórios:

```
router bgp 65000
 address-family ipv4 unicast
  table-policy IMPORT-FILTER
  maximum-paths ebgp 4
 neighbor <upstream1>
  remote-as <ASN>
  description "Upstream A - 10G"
  password <md5>
  address-family ipv4 unicast
   route-policy ACCEPT-ANY in
   route-policy ANNOUNCE-OUR-PREFIXES out
   soft-reconfiguration inbound always
   maximum-prefix 1500000 90 restart 5
```

Diagnóstico padrão "internet caiu":

```
show bgp ipv4 unicast summary
show bgp ipv4 unicast neighbors <peer> received-routes | utility wc -l
show route summary
show platform hardware fpd | inc Memory
```

Se `Established` mas tabela vazia: route-policy IN bloqueando. Se quedas frequentes: BFD timer agressivo demais ou flapping de upstream.

### CGNAT em IOS-XE / IOS-XR (CGv6)

IOS-XR tem **CGv6** dedicado em line-card específica (NCS5500 + ServiceInfra Edge):

```
service cgn cgn1
 service-location preferred-active 0/2/CPU0
 inside-vrf privado
  map address-pool 200.x.x.0/24
  protocol tcp
   session active timeout 120
   session init timeout 30
```

Sempre exporte translation logs (Netflow v9 ou syslog) — exigência legal de retenção 12 meses.

### MPLS L3VPN para clientes corporativos

```
vrf definition CLIENTE-ACME
 rd 65000:1001
 address-family ipv4
  route-target export 65000:1001
  route-target import 65000:1001
!
interface GigabitEthernet0/0/1
 vrf forwarding CLIENTE-ACME
 ip address 10.1.1.1 255.255.255.252
```

Diagnóstico VPN cliente:

```
show ip route vrf CLIENTE-ACME
show bgp vpnv4 unicast vrf CLIENTE-ACME
show mpls forwarding-table vrf CLIENTE-ACME
show ip cef vrf CLIENTE-ACME <prefix>
```

### Anti-DDoS via blackhole BGP

Padrão: comunidade do upstream que injeta nullroute. Você anuncia /32 do alvo com a community:

```
ip community-list standard BLACKHOLE permit <ASN>:<comm>
route-map TO-UPSTREAM permit 10
 match ip address prefix-list BLACKHOLE-TARGETS
 set community <ASN>:<comm>
```

Use só durante ataque ativo — depois remova. Manter blackhole permanente vira buraco de alcance.

### Operações típicas via WhatsApp (NetAgent)

| Pedido | Ação |
|---|---|
| "Peer X dropou" | `show bgp neighbors <ip>` + análise de last error |
| "Latência alta no link Y" | `show interface <if>` + drops/errors, `show platform hardware qfp` |
| "Anunciar nullroute pro IP atacado" | confirmar IP, route-map + redistribute static |
| "Backup da config" | `show running | redirect bootflash:backup.txt` + scp out |
| "Cliente VPN sem conectar" | `show bgp vpnv4 vrf <cliente>` + traceroute em VRF |

## Report template

```markdown
## Diagnóstico: <título>
**Sintoma:** <linha>
**Plataforma:** IOS-XE 17.6 / IOS-XR 7.x / NX-OS 9.x

**Comandos:**
- `<cmd>` → <resultado>

**Análise:** <2-4 linhas>
**Próximos passos:** <bullets>
**Rollback:** `<comandos>`
```
