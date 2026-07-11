---
name: pfsense-ops
description: "Senior pfSense firewall engineer for ISP/MSP operations. Use when the user asks to diagnose, audit, automate, monitor, or operate pfSense CE/Plus firewalls via REST API package, SSH/CLI, WebGUI read-only guidance, or MCP: firewall rules, aliases, NAT, VLANs, interfaces, DHCP, Unbound DNS, gateways, routes, VPN status, pf states/logs, backups, services, packages, CARP/HA and safe change workflows."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [pfsense, firewall, networking, api, mcp, vpn, nat, dns, dhcp]
    related_skills: [opnsense-ops, fortigate-fortios, sophos-firewall-ops, blockbit-firewall-ops, mikrotik-ops]
    source_research:
      - https://github.com/gensecaihq/pfsense-mcp-server
      - https://github.com/antonio-mello-ai/mcp-pfsense
      - https://github.com/stepanov1975/pfsense-mcp-server
      - https://github.com/pfrest/pfSense-pkg-RESTAPI
      - https://github.com/devinbarry/pyfsense-client
---

# pfSense Operations

Senior firewall/network engineer for pfSense CE/Plus in ISP/MSP environments. Speak Brazilian Portuguese with the user; keep pfSense, FreeBSD, `pfctl`, REST API and CLI syntax in original form.

This skill is a Hermes-native operational playbook, adapted from public pfSense REST/API/MCP patterns and sanitized for the Fórum Telecom workflow. It is not a copy of third-party agent content. Default stance: **read-only first, snapshot before change, explicit confirmation for risky actions, validate after every action**.

## When to use

Use for pfSense CE/Plus tasks:

- firewall/NAT/alias/rule audit;
- DHCP leases/static mappings, Unbound DNS overrides;
- gateway/WAN status, routes, ARP/NDP, interface/VLAN checks;
- VPN status/troubleshooting: IPsec, OpenVPN, WireGuard when installed;
- CARP/HA status, services, package inventory;
- safe API/MCP automation with pfSense REST API package;
- SSH diagnostics on FreeBSD/pfSense when API is unavailable.

Use `opnsense-ops` for OPNsense. They are related but API paths and service tooling differ.

## API/MCP support status

pfSense CE/Plus historically does not expose one universal built-in API on all installs. For MCP/API automation, prefer the REST API package (`pfSense-pkg-RESTAPI`, also known as pfrest) or a vetted internal wrapper.

A Fórum Telecom MCP skeleton is published in this repository:

```text
mcp/pfsense-api-mcp
```

It is read-only by default and exposes safe tools for config status, endpoint catalog, generic REST request with write guard, common system/firewall/DHCP checks, and sanitized outputs.

## Connection variables

Store secrets in `.env`, Hermes env, or device vault — never paste credentials in group chat.

| Variable | Purpose |
|---|---|
| `PFSENSE_BASE_URL` | Base URL, e.g. `https://fw.example.com` |
| `PFSENSE_USERNAME` / `PFSENSE_PASSWORD` | Username/password auth when used by the API package |
| `PFSENSE_API_KEY` / `PFSENSE_API_SECRET` | API key auth when supported/configured |
| `PFSENSE_TOKEN` | Bearer/JWT token when supported |
| `PFSENSE_VERIFY_SSL` | `true` for valid cert, `false` only on trusted internal/self-signed labs |
| `PFSENSE_TIMEOUT` | HTTP timeout in seconds |
| `PFSENSE_READ_ONLY` | keep `true` unless a controlled change is explicitly approved |
| `PFSENSE_MASK_SENSITIVE` | keep `true` to redact secrets/PII in outputs |
| `PFSENSE_SSH_HOST` / `PFSENSE_SSH_USER` | SSH diagnostics when API is not available |

## Mandatory workflow

### 1. Identify

Confirm version, platform, access method and target object before changing anything.

REST/API examples, exact paths depend on the installed API package version:

```bash
curl -sk -u "$PFSENSE_USERNAME:$PFSENSE_PASSWORD" "$PFSENSE_BASE_URL/api/v2/status/system"
curl -sk -u "$PFSENSE_USERNAME:$PFSENSE_PASSWORD" "$PFSENSE_BASE_URL/api/v2/interface"
curl -sk -u "$PFSENSE_USERNAME:$PFSENSE_PASSWORD" "$PFSENSE_BASE_URL/api/v2/firewall/rule"
```

SSH/CLI read-only probes:

```sh
cat /etc/version
uname -a
ifconfig
netstat -rn
pfctl -s info
pfctl -s rules
pfctl -s nat
pfctl -s state | head -50
clog /var/log/filter.log | tail -100
```

### 2. Snapshot before mutation

Before firewall/NAT/DHCP/DNS/VPN changes, save a configuration backup.

Common CLI backup:

```sh
cp /cf/conf/config.xml /cf/conf/config.xml.pre-hermes-$(date +%Y%m%d-%H%M%S)
```

If using API package, use its config backup endpoint if available. Never paste full `config.xml` in chat; it may contain hashes, certificates, VPN secrets and tokens.

### 3. Apply cautiously

Prefer API/MCP operations with strict schemas over ad-hoc shell. Make the smallest change possible. For rule/NAT/alias changes:

1. identify existing object IDs/descriptions;
2. check conflicts and references;
3. backup config;
4. apply one delta;
5. reload/apply filter only when needed;
6. validate with API + `pfctl` + logs.

### 4. Validate

```sh
pfctl -s rules | grep -i '<description-or-ip>'
pfctl -s nat | grep -i '<port-or-ip>'
pfctl -s state | grep '<ip>'
clog /var/log/filter.log | grep '<ip>' | tail -50
```

For WAN/gateway checks:

```sh
netstat -rn
ifconfig <wan>
ping -S <wan-ip> 8.8.8.8
dig @1.1.1.1 google.com
```

### 5. Report

Report summarized evidence only:

```markdown
## Operação pfSense: <título>
**Firewall:** <hostname/IP mascarado se necessário>
**Objeto:** <rule/alias/NAT/interface/service>

**Antes:** <estado resumido>
**Ação:** <endpoint/comando usado>
**Depois:** <validação objetiva>
**Rollback:** <backup/savepoint/caminho de reversão>
**Risco restante:** <se houver>
```

## Common recipes

### Audit rules for one customer/IP

1. Search aliases and rules.
2. Check states/logs for the exact IP.
3. Confirm source interface: pfSense filters traffic on the interface where it enters.

```sh
pfctl -s rules | grep -i '<ip-or-alias>'
pfctl -s state | grep '<ip>'
clog /var/log/filter.log | grep '<ip>' | tail -100
```

### Add port forward safely

- Confirm WAN, internal target IP, protocol and source restriction.
- Check conflict with existing NAT/rules.
- Backup config.
- Add NAT rule and associated pass rule.
- Validate with `pfctl -s nat`, logs and external test.

Do not expose management services (pfSense GUI, SSH, RDP, Proxmox, Winbox, database) to WAN without explicit confirmation and source allowlist.

### Inter-VLAN routing

- Check VLAN interface status and IPs.
- Rules belong on source interface/VLAN.
- Inter-VLAN traffic usually should not use outbound NAT.
- Validate states/logs, not only ping.

### DNS/DHCP

- Identify active resolver/DHCP service.
- Backup/list existing override/reservation.
- Change one mapping.
- Restart/reload only the affected service.
- Validate from a client path.

## Safety rules

### Never without literal confirmation

- reboot, halt, poweroff;
- firmware/package upgrade;
- restore/import config XML;
- deleting rules/NAT/aliases/interfaces/VLANs/certificates/VPNs;
- changing WAN/LAN assignments, GUI port/certificate, anti-lockout, admin access;
- disabling firewall or running `pfctl -d`;
- clearing all states on production firewall;
- exposing management ports to WAN;
- direct `config.xml` edits.

Confirmation pattern:

> Operação perigosa: `<ação>`  
> Impacto: <risco em uma frase>  
> Para executar, responda exatamente: `CONFIRMO <ação>`

### Always warn before

- applying firewall remotely where management access may drop;
- changing rules on customer/source VLANs;
- restarting DNS/DHCP/VPN during business hours;
- packet capture on high throughput links;
- using `PFSENSE_VERIFY_SSL=false` outside trusted internal network.

## MCP quick start for students

```bash
cd mcp/pfsense-api-mcp
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
cp .env.example .env
# preencher PFSENSE_BASE_URL e credenciais no .env, sem colar no grupo
python server.py
```

In Hermes/Claude-compatible MCP config, run the server through the venv Python and pass env vars. Keep `PFSENSE_READ_ONLY=true` until testing is complete.

## When NOT to use

- OPNsense-specific operations: use `opnsense-ops`.
- MikroTik, FortiGate, Sophos, Blockbit, Cisco, Huawei, Proxmox, Zabbix: use the specific skill.
- Password recovery, bypassing firewall authentication, or exposing secrets.
