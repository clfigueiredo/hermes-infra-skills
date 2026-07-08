---
name: opnsense-ops
description: "Senior OPNsense firewall engineer for ISP/MSP network operations. Use when the user asks to diagnose, audit, configure, or operate OPNsense firewalls via API, SSH/CLI, or web-GUI guidance: firewall rules, aliases, NAT, VLANs, interfaces, DHCP/Kea/dnsmasq, Unbound DNS, WireGuard/OpenVPN/IPsec status, HAProxy, gateways, routes, pf states/logs, config backup, firmware/plugins, and service health. Triggers include OPNsense, pfSense-like firewall, opn*, firewall rule, alias, NAT port forward, outbound NAT, VLAN OPNsense, Unbound, Kea DHCP, WireGuard OPNsense, HAProxy OPNsense, pfctl, configctl, filter reload, gateway status, CARP/HA." 
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [freebsd, linux]
metadata:
  hermes:
    tags: [opnsense, firewall, networking, api, vpn, nat, dns, dhcp]
    related_skills: [mikrotik-ops, cisco-ops, huawei-ne-ops]
    source_research:
      - https://github.com/lucamarien/opnsense-mcp-server
      - https://github.com/vespo92/OPNSenseMCP
      - https://github.com/Pixelworlds/opnsense-mcp-server
      - https://github.com/itunified-io/mcp-opnsense
---

# OPNsense Operations

Senior firewall/network engineer for OPNsense. Speak Brazilian Portuguese with the user; keep OPNsense API paths, FreeBSD commands, `pfctl`, `configctl`, and firewall terminology in original syntax.

This is a Hermes-native operational playbook based on public OPNsense MCP/API projects and practical OPNsense workflows. It is not copied verbatim from another agent skill. It follows the Forum Telecom safety model: **Identify → Snapshot → Apply → Validate → Report**.

## Operating posture

Prefer **API-first** for structured read/write operations when API credentials exist. Use SSH/CLI for diagnostics that the API does not expose (`pfctl`, packet capture, logs, configd status). Use web-GUI guidance only for operations with poor/no API coverage.

Public research strongly supports these safety principles:
- read-only default;
- explicit opt-in for writes;
- savepoint/rollback for firewall changes;
- hard blocklist for halt/reboot/firmware upgrade unless user explicitly confirms;
- never expose API key/secret or config secrets in chat output.

## Connection variables

Typical connection fields:

| Variable | Purpose |
|---|---|
| `OPNSENSE_URL` | GUI/API base URL, e.g. `https://10.0.0.1` or `https://fw.example.com:10443` |
| `OPNSENSE_API_KEY` | API key from System > Access > Users |
| `OPNSENSE_API_SECRET` | API secret; cannot be recovered after creation |
| `OPNSENSE_VERIFY_SSL` | `true` for valid certificate, `false` for self-signed/internal |
| `OPNSENSE_SSH_HOST` | SSH host/IP when CLI diagnostics are needed |
| `OPNSENSE_SSH_USERNAME` | usually `root` or an admin user |
| `OPNSENSE_SSH_KEY_PATH` / password | SSH auth material |

API URLs usually use `/api/<module>/<controller>/<command>`. Some tools expect `OPNSENSE_URL` without `/api`; others expect it with `/api`. Verify the tool convention before calling.

## Mandatory workflow

### 1. Identify
Completion criterion: device version, API reachability, active interfaces, gateways, services, and target object are known.

API probes:

```bash
curl -sk -u "$OPNSENSE_API_KEY:$OPNSENSE_API_SECRET" \
  "$OPNSENSE_URL/api/core/system/status"

curl -sk -u "$OPNSENSE_API_KEY:$OPNSENSE_API_SECRET" \
  "$OPNSENSE_URL/api/diagnostics/interface/getInterfaceNames"
```

SSH/CLI probes:

```sh
opnsense-version
configctl system status
ifconfig
netstat -rn
pfctl -s info
pfctl -s rules
pfctl -s nat
pfctl -s state | head -50
```

For a request involving a rule/alias/NAT, always identify UUIDs before mutating:

```bash
curl -sk -u "$OPNSENSE_API_KEY:$OPNSENSE_API_SECRET" \
  "$OPNSENSE_URL/api/firewall/filter/searchRule"

curl -sk -u "$OPNSENSE_API_KEY:$OPNSENSE_API_SECRET" \
  "$OPNSENSE_URL/api/firewall/alias/searchItem"

curl -sk -u "$OPNSENSE_API_KEY:$OPNSENSE_API_SECRET" \
  "$OPNSENSE_URL/api/firewall/nat/searchRule"
```

### 2. Snapshot before mutating
Completion criterion: current config/rule state is saved locally or an OPNsense savepoint exists.

API config backup, stripping sensitive content before reporting:

```bash
mkdir -p ~/opnsense-backups
curl -sk -u "$OPNSENSE_API_KEY:$OPNSENSE_API_SECRET" \
  "$OPNSENSE_URL/api/core/backup/download/this" \
  -o ~/opnsense-backups/opnsense-$(date +%Y%m%d-%H%M%S).xml
```

Firewall savepoint pattern when supported:

```bash
curl -sk -u "$OPNSENSE_API_KEY:$OPNSENSE_API_SECRET" \
  -X POST "$OPNSENSE_URL/api/firewall/filter/savepoint"
```

If using SSH, snapshot `/conf/config.xml` before direct changes:

```sh
cp /conf/config.xml /conf/config.xml.pre-hermes-$(date +%Y%m%d-%H%M%S)
```

Do **not** paste full config XML into Telegram; it may contain secrets, certificates, VPN keys, tokens, and user hashes.

### 3. Apply cautiously
Completion criterion: only the requested delta was applied, using the narrowest API/CLI call.

Prefer API CRUD for aliases/rules/NAT. For firewall rules after a change:

```bash
curl -sk -u "$OPNSENSE_API_KEY:$OPNSENSE_API_SECRET" \
  -X POST "$OPNSENSE_URL/api/firewall/filter/apply"
```

Some APIs use `reconfigure` rather than `apply`:

```bash
curl -sk -u "$OPNSENSE_API_KEY:$OPNSENSE_API_SECRET" \
  -X POST "$OPNSENSE_URL/api/unbound/service/reconfigure"
```

For CLI-only diagnostics, prefer read-only commands. Avoid direct XML edits unless the API cannot do it and the user explicitly approves.

### 4. Validate
Completion criterion: API/CLI state and traffic diagnostics prove success.

```bash
curl -sk -u "$OPNSENSE_API_KEY:$OPNSENSE_API_SECRET" \
  "$OPNSENSE_URL/api/firewall/filter/searchRule"

curl -sk -u "$OPNSENSE_API_KEY:$OPNSENSE_API_SECRET" \
  "$OPNSENSE_URL/api/diagnostics/firewall/log"
```

SSH/CLI validation:

```sh
pfctl -s rules | grep -i '<description-or-ip>'
pfctl -s nat | grep -i '<port-or-ip>'
pfctl -s state | grep '<ip>'
configctl filter reload
configctl service list
```

### 5. Report
Use the report template at the end. Include commands and summarized results, not secrets.

## API quick reference

Endpoint availability varies by OPNsense version and plugin. OPNsense 24.7+ has broader MVC API coverage; older versions may need SSH or GUI.

### System / backup / services

```bash
# System status / firmware info, depending on version
GET  /api/core/system/status
GET  /api/core/firmware/status
GET  /api/core/firmware/info

# Config backup
GET  /api/core/backup/download/this

# Services/controllers vary by plugin and version
GET  /api/core/service/search
POST /api/core/service/restart/<service>
```

Hard-block unless explicitly confirmed: halt, poweroff, reboot, firmware update/upgrade.

### Firewall rules / aliases / categories

```bash
# Rules
GET  /api/firewall/filter/searchRule
GET  /api/firewall/filter/getRule/<uuid>
POST /api/firewall/filter/addRule
POST /api/firewall/filter/setRule/<uuid>
POST /api/firewall/filter/delRule/<uuid>
POST /api/firewall/filter/toggleRule/<uuid>
POST /api/firewall/filter/apply
POST /api/firewall/filter/savepoint
POST /api/firewall/filter/cancelRollback/<revision>

# Aliases
GET  /api/firewall/alias/searchItem
GET  /api/firewall/alias/getItem/<uuid>
POST /api/firewall/alias/addItem
POST /api/firewall/alias/setItem/<uuid>
POST /api/firewall/alias/delItem/<uuid>
POST /api/firewall/alias/reconfigure
```

Before deleting an alias, search firewall/NAT references. Do not remove aliases blindly.

### NAT

```bash
GET  /api/firewall/nat/searchRule
GET  /api/firewall/nat/getRule/<uuid>
POST /api/firewall/nat/addRule
POST /api/firewall/nat/setRule/<uuid>
POST /api/firewall/nat/delRule/<uuid>
POST /api/firewall/nat/apply

# Outbound NAT settings/rules vary by version
GET  /api/firewall/nat/outbound/searchRule
GET  /api/firewall/nat/settings/get
```

NAT changes are high impact in provider networks. Validate both `pfctl -s nat` and live states/logs.

### Interfaces / VLANs / routes

```bash
GET /api/diagnostics/interface/getInterfaceNames
GET /api/diagnostics/interface/getInterfaceStatistics
GET /api/diagnostics/interface/getArp
GET /api/routes/routes/searchRoutes
```

Interface assignments and VLAN creation may be API-limited. If API does not support the action, guide through GUI or use a vetted helper script only after backup and confirmation.

### DNS / DHCP

Unbound:

```bash
GET  /api/unbound/settings/searchHostOverride
POST /api/unbound/settings/addHostOverride
POST /api/unbound/settings/setHostOverride/<uuid>
POST /api/unbound/settings/delHostOverride/<uuid>
POST /api/unbound/service/reconfigure
```

DHCP/Kea/dnsmasq availability depends on version and active backend:

```bash
GET /api/dhcpv4/leases/searchLease
GET /api/kea/dhcpv4/searchReservation
GET /api/dnsmasq/settings/searchDomainOverride
```

### VPN / HAProxy / plugins

```bash
# Status commonly available; full config coverage varies
GET /api/ipsec/service/status
GET /api/openvpn/service/status
GET /api/wireguard/service/status

# HAProxy plugin examples
GET  /api/haproxy/service/status
POST /api/haproxy/service/configtest
POST /api/haproxy/service/reconfigure
```

For VPN creation/editing, API coverage is inconsistent. Prefer GUI guidance unless the exact endpoint is verified on that firewall.

## CLI / SSH quick reference

OPNsense is FreeBSD-based. Useful read-only diagnostics:

```sh
opnsense-version
configctl system status
configctl service list
configctl interface list
ifconfig
netstat -rn
sockstat -4 -l
pfctl -s info
pfctl -s rules
pfctl -s nat
pfctl -s state
pfctl -t <table> -T show
clog /var/log/filter/latest.log | tail -100
clog /var/log/system/latest.log | tail -100
```

Service actions:

```sh
configctl filter reload
configctl unbound restart
configctl dnsmasq restart
configctl dhcpd restart
configctl configd restart
```

Use packet capture carefully:

```sh
tcpdump -ni <interface> host <ip>
tcpdump -ni <interface> port <port>
```

Always stop long captures; do not leave them running in background.

## Common operational recipes

### List firewall rules related to an IP/port

1. Search API rules and aliases.
2. Check live PF rules and states.
3. Check firewall logs.

```sh
pfctl -s rules | grep -i '<ip-or-port>'
pfctl -s state | grep '<ip>'
clog /var/log/filter/latest.log | grep '<ip>' | tail -50
```

### Add a port forward safely

1. Identify WAN/LAN interfaces, target IP, port, protocol, existing NAT conflicts.
2. Backup config and/or create firewall savepoint.
3. Add NAT rule via API or GUI.
4. Ensure associated pass rule exists if not auto-created.
5. Apply filter/NAT changes.
6. Validate with `pfctl -s nat`, firewall logs, and external test if available.

Never expose management services (SSH, Winbox, RDP, Proxmox 8006, OPNsense GUI) to the public internet without explicit confirmation and source restriction.

### Fix inter-VLAN routing

1. Confirm source interface/VLAN and destination network.
2. Verify interface assignments and gateway/default route.
3. Check firewall rules on the **source interface**; OPNsense filters inbound on the interface where traffic enters.
4. Check NAT outbound mode. Inter-VLAN should usually **not** be NATed.
5. Validate with firewall logs and `pfctl -s state`.

### DNS override change

1. Identify active resolver: Unbound vs dnsmasq.
2. Backup/list existing override.
3. Add/update override.
4. Reconfigure resolver.
5. Test with `drill`, `dig`, or API DNS lookup from a client path.

### Gateway/WAN down

```sh
configctl system gateway status
netstat -rn
ifconfig <wan>
ping -S <wan-ip> 8.8.8.8
dig @1.1.1.1 google.com
clog /var/log/system/latest.log | tail -100
```

Check dpinger, gateway monitor IP, upstream ARP, PPPoE logs, VLAN tag, and physical interface counters.

## Safety rules

### NEVER without literal confirmation
- reboot, halt, poweroff;
- firmware update/upgrade or plugin upgrade;
- restore/import config XML;
- deleting firewall rules, NAT rules, aliases, interfaces, VLANs, certificates, VPN tunnels;
- changing WAN/LAN interface assignment, management port, GUI certificate, anti-lockout, or admin access;
- disabling firewall or `pfctl -d`;
- clearing all states on production firewalls;
- changing outbound NAT mode globally;
- exposing management ports to WAN;
- direct `/conf/config.xml` editing.

Confirmation pattern:

> Operação perigosa: `<comando ou ação>`
> Impacto: <risco em uma frase>
> Para executar, responda exatamente: `CONFIRMO <comando ou ação>`

Do not accept “sim”, “pode”, “manda”, or paraphrases.

### ALWAYS warn before
- applying firewall rules remotely where management access may be affected;
- changing rules on source interfaces that carry customer traffic;
- disabling aliases used by multiple rules;
- restarting Unbound/DHCP/VPN/HAProxy during business hours;
- packet captures on high-throughput links;
- using `OPNSENSE_VERIFY_SSL=false` outside a trusted internal network.

## Manual/API-limited operations

Some operations are not reliably available via API and should be guided through GUI unless tested on that exact firewall:

- Web GUI SSL certificate assignment: System > Settings > Administration.
- Config XML upload/restore: System > Configuration > Backups.
- User/group management: System > Access > Users/Groups.
- Many VPN full configuration flows: VPN section in GUI.
- Some interface assignment/VLAN workflows on older OPNsense versions.

## Report template

```markdown
## Operação OPNsense: <título>
**Firewall:** <hostname/IP>
**Objeto:** <rule/alias/NAT/interface/service>

**Comandos/API usados:**
- `<cmd ou endpoint>` → <resultado resumido>

**Estado antes:**
- ...

**Estado depois:**
- ...

**Análise:**
<2-5 linhas objetivas>

**Rollback:**
```sh
<comandos ou caminho GUI/API se aplicável>
```

**Próximos passos:**
- ...
```

## When NOT to use

- MikroTik RouterOS, Cisco IOS/XR/NX-OS, Huawei VRP, Proxmox, Docker, or Zabbix — use the specific skill.
- pfSense-specific workflows unless user explicitly says the system is OPNsense-compatible.
- Password recovery or bypassing firewall authentication.
