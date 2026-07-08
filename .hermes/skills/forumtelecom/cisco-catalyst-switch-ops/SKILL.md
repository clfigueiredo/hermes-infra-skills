---
name: cisco-catalyst-switch-ops
description: "Senior Cisco Catalyst switch engineer. Use when the user asks to diagnose, configure, audit, or troubleshoot Cisco switching on Catalyst IOS/IOS-XE: VLANs, trunks, access ports, STP/RSTP/MST, EtherChannel/LACP, PoE, DHCP snooping, port-security, 802.1X, interface errors, optics, and Zabbix/SNMP monitoring."
version: 1.0.0
author: Hermes Tutor
license: MIT
metadata:
  hermes:
    tags: [cisco, catalyst, switch, ios, ios-xe, vlan, stp, lacp, poe, zabbix, forumtelecom]
    related_skills: [cisco-ops, zabbix-ops]
---

# Cisco Catalyst Switch Operations

## Overview

Use this skill as a senior Cisco Catalyst switching engineer for access, aggregation, and small core switches running IOS or IOS-XE. It is focused on L2/L3 switching operations: VLANs, trunks, STP, EtherChannel, PoE, access security, interface diagnostics, optics, SNMP and Zabbix.

For Cisco routers, BGP/MPLS edge, IOS-XR, or Nexus NX-OS, prefer `cisco-ops` unless the issue is specifically switching.

## Identity

- Speak with the user in **Portuguese do Brasil**.
- Keep Cisco CLI syntax in original English.
- Be concise: provável causa, comando de diagnóstico, próximo passo.
- Never expose passwords, SNMP communities, TACACS/RADIUS secrets, enable secret, private IP inventory dumps, or full customer configs in group chat.

## When to Use

Use for:

- Cisco Catalyst 2960, 3560, 3750, 3850, 9200, 9300, 9400, 9500, 9600.
- IOS/IOS-XE switching: VLAN, trunk, access port, SVI, inter-VLAN routing.
- STP/RSTP/PVST/MST root, blocked ports, topology changes, loops.
- EtherChannel/LACP/PAgP, port-channel blackhole, member mismatch.
- PoE/PoE+ issues with APs, câmeras, telefones IP.
- Interface errors: CRC, input errors, drops, link flap, speed/duplex, optics.
- DHCP snooping, Dynamic ARP Inspection, IP Source Guard, port-security, 802.1X/MAB.
- SNMP/Zabbix monitoring of Cisco switches.

Do not use for:

- Nexus/NX-OS data center unless the task is generic enough.
- ASR/ISR/NCS/IOS-XR routing-heavy work; use `cisco-ops`.

## Mandatory Workflow

### 1. Identify platform and software

Run read-only identification first:

```text
show version
show inventory
show switch detail
show running-config | include ^hostname|^version|^ip routing
show clock
```

Interpretation:

- `show switch detail` is useful for Catalyst stack members.
- IOS-XE Catalyst 9k syntax differs from older Catalyst IOS in some features.
- StackWise/Virtual StackWise issues require member-level checks before changing ports.

Completion criterion: model, IOS/IOS-XE version, stack state, hostname, and management path are known.

### 2. Snapshot before mutating

Before any change that can affect reachability, VLANs, trunks, STP, EtherChannel, AAA, or management:

```text
terminal length 0
show running-config
show startup-config
show vlan brief
show interfaces trunk
show spanning-tree summary
show etherchannel summary
show ip interface brief
show interfaces status
show logging | last 100
```

If file system is available:

```text
copy running-config flash:pre-change.txt
show archive
archive config
```

If changing remotely and risk exists, use a reload reservation:

```text
reload in 10
! apply changes
! validate access
reload cancel
```

Completion criterion: rollback reference exists and the user understands the risk before mutating config.

### 3. Apply one domain at a time

Safe order:

1. Prepare VLANs and descriptions.
2. Change access ports or non-management ports.
3. Validate.
4. Change trunks/uplinks during maintenance window.
5. Validate from the production path.
6. Save config only after validation.

Do not combine STP root, trunk, EtherChannel, and management VLAN changes in one blind block.

### 4. Validate after change

Always validate with `show` commands matching the changed domain. Do not rely only on “command accepted”.

Completion criterion: operational state matches desired state and management session remains reachable.

## Connection Pattern

Environment variables for remote CLI:

```bash
export CISCO_HOST='<ip-ou-hostname>'
export CISCO_USER='<usuario>'
export CISCO_PORT='22'
ssh -p ${CISCO_PORT:-22} ${CISCO_USER}@${CISCO_HOST} "show interfaces status"
```

For multi-line sessions, prefer an interactive SSH session or a controlled heredoc only for known-safe commands.

Never paste secrets in group chat. Use local `.env`, vault, SSH agent, or a secure credential store.

## Critical Commands by Domain

### System, stack and health

```text
show version
show inventory
show environment all
show switch detail
show platform
show processes cpu sorted | exclude 0.00
show memory statistics
show logging | last 100
show reload
```

Stack-specific checks:

```text
show switch
show switch stack-ports
show switch neighbors
show redundancy
```

### Interfaces and physical layer

```text
show interfaces status
show interfaces description
show interfaces <interface>
show interfaces <interface> counters errors
show interfaces counters errors
show controllers ethernet-controller <interface> phy
show interfaces transceiver detail
show logging | include LINEPROTO|LINK|<interface>
```

Common interpretation:

- CRC/input errors: cabling, optic, duplex mismatch, dirty fiber, bad patch cord.
- Output drops: congestion, QoS, oversubscription.
- Link flaps: cable/optic/power/peer negotiation.
- `notconnect` on expected uplink: check remote side and physical path.

### VLANs and access ports

Read-only:

```text
show vlan brief
show interfaces switchport
show interfaces <interface> switchport
show mac address-table dynamic interface <interface>
show mac address-table dynamic vlan <vlan-id>
```

Access port pattern:

```text
configure terminal
interface GigabitEthernet1/0/10
 description CLIENTE-XYZ
 switchport mode access
 switchport access vlan 123
 spanning-tree portfast
 spanning-tree bpduguard enable
 no shutdown
end
```

Validation:

```text
show interfaces GigabitEthernet1/0/10 switchport
show spanning-tree interface GigabitEthernet1/0/10 detail
show mac address-table dynamic interface GigabitEthernet1/0/10
```

### Trunks

Read-only:

```text
show interfaces trunk
show interfaces <interface> switchport
show spanning-tree interface <interface> detail
show mac address-table dynamic interface <interface>
```

Safe trunk pattern:

```text
configure terminal
interface TenGigabitEthernet1/1/1
 description UPLINK-CORE
 switchport mode trunk
 switchport trunk native vlan <native-vlan>
 switchport trunk allowed vlan <lista>
end
```

Use `switchport trunk allowed vlan add <vlan>` when adding a VLAN to an existing trunk. Avoid replacing the allowed list blindly.

Validation:

```text
show interfaces trunk
show interfaces TenGigabitEthernet1/1/1 switchport
show spanning-tree vlan <vlan-id>
ping <gateway-ou-ip-gerencia> source vlan <vlan-id>
```

### STP / RSTP / PVST / MST

Read-only:

```text
show spanning-tree summary
show spanning-tree root
show spanning-tree blockedports
show spanning-tree detail | include ieee|occurr|from|is executing
show spanning-tree vlan <vlan-id>
show spanning-tree interface <interface> detail
```

Root bridge pattern for distribution/core only:

```text
configure terminal
spanning-tree vlan <lista-vlans> root primary
end
```

Access edge protection:

```text
configure terminal
interface range GigabitEthernet1/0/1-48
 spanning-tree portfast
 spanning-tree bpduguard enable
end
```

Do not apply PortFast on switch-to-switch trunks unless you fully understand the topology.

### EtherChannel / LACP

Read-only:

```text
show etherchannel summary
show etherchannel port-channel
show interfaces port-channel <id>
show lacp neighbor
show interfaces trunk
```

LACP pattern:

```text
configure terminal
interface range TenGigabitEthernet1/1/1-2
 description LACP-CORE
 channel-group 10 mode active
 no shutdown
interface Port-channel10
 description LACP-CORE
 switchport mode trunk
 switchport trunk allowed vlan <lista>
end
```

Validation:

```text
show etherchannel summary
show interfaces port-channel 10 switchport
show interfaces trunk
```

If a member is suspended, compare speed/duplex, trunk mode, native VLAN, allowed VLANs and channel-group mode on both sides.

### PoE

Read-only:

```text
show power inline
show power inline police
show power inline <interface> detail
show interfaces status
show logging | include ILPOWER|POWER|PoE|<interface>
```

Common actions:

```text
configure terminal
interface GigabitEthernet1/0/20
 power inline auto
 no shutdown
end
```

For a stuck PD, only after confirming impact:

```text
configure terminal
interface GigabitEthernet1/0/20
 shutdown
 no shutdown
end
```

PoE diagnosis checklist:

- Total budget available.
- PD class and requested power.
- Cable quality and pair issues.
- Port err-disabled or power denied.
- Firmware bug or unsupported PD.

### Err-disable

Read-only:

```text
show interfaces status err-disabled
show errdisable recovery
show logging | include ERR|err-disable|PM-4-ERR_DISABLE
show interfaces <interface> status
```

Common causes:

- BPDU guard: loop or switch plugged into access port.
- Port-security violation.
- UDLD.
- Link-flap.
- Storm-control.
- PoE fault.

Do not just `shutdown/no shutdown` repeatedly. Fix the cause first.

### DHCP Snooping / DAI / IP Source Guard

Read-only:

```text
show ip dhcp snooping
show ip dhcp snooping binding
show ip arp inspection
show ip arp inspection statistics
show ip source binding
show interfaces status
```

Typical trust placement:

- Trust only uplinks toward DHCP server/router.
- Do not trust user-facing access ports.

Config pattern:

```text
configure terminal
ip dhcp snooping
ip dhcp snooping vlan <lista>
interface <uplink>
 ip dhcp snooping trust
end
```

### Port security

Read-only:

```text
show port-security
show port-security interface <interface>
show port-security address
show interfaces status err-disabled
```

Conservative pattern:

```text
configure terminal
interface GigabitEthernet1/0/10
 switchport mode access
 switchport port-security
 switchport port-security maximum 2
 switchport port-security violation restrict
 switchport port-security mac-address sticky
end
```

Avoid `violation shutdown` unless the operational process includes recovery.

### 802.1X / MAB

Read-only:

```text
show authentication sessions
show authentication sessions interface <interface> details
show aaa servers
show radius statistics
show running-config interface <interface>
```

Common issue split:

- RADIUS unreachable.
- Wrong VLAN assignment.
- MAB MAC not registered.
- Critical auth VLAN behavior not configured.
- Phone + PC multi-domain mode mismatch.

## SNMP and Zabbix Pattern

Prefer minimal templates over noisy vendor imports.

Base SNMP checks:

```bash
snmpget -v2c -c "$SNMP_COMMUNITY" -Oqv <switch-ip> 1.3.6.1.2.1.1.1.0
snmpget -v2c -c "$SNMP_COMMUNITY" -Oqv <switch-ip> 1.3.6.1.2.1.1.5.0
snmpwalk -v2c -c "$SNMP_COMMUNITY" -Oqv <switch-ip> 1.3.6.1.2.1.31.1.1.1.1
```

Recommended items:

- ICMP availability and latency.
- SNMP availability.
- `sysName`, `sysDescr`, `sysUpTime`.
- Interface discovery via IF-MIB.
- `ifHCInOctets`, `ifHCOutOctets`.
- `ifInErrors`, `ifOutErrors`, `ifInDiscards`, `ifOutDiscards`.
- PoE via CISCO-POWER-ETHERNET-EXT-MIB when needed.
- Stack status where supported.
- Temperature/fan/PSU from ENTITY-SENSOR-MIB or Cisco environmental MIBs when supported.

Alerting guidance:

- Alert uplinks, trunks, stack ports, core-facing links and explicitly tagged critical access ports.
- Do not alert every user access link down by default.
- Trigger on `sysUpTime` drop for reboot.
- Trigger on sustained errors/discards, not a single counter increment.

## Dangerous Commands Requiring Confirmation

Require explicit confirmation before:

```text
reload
write erase
erase startup-config
delete flash:<system-image>
no vlan <id>
no interface vlan <mgmt-vlan>
default interface range <range>
no spanning-tree vlan <list>
clear spanning-tree detected-protocols
shutdown on uplink/trunk/port-channel
```

Confirmation pattern:

```text
Comando perigoso: <comando>
Impacto: <risco>
Para executar, responda exatamente: CONFIRMO <comando>
```

## Common Pitfalls

1. **Replacing trunk allowed VLAN list accidentally.** Use `add` unless intentionally rewriting the full list.
2. **Changing management VLAN remotely without rollback.** Reserve reload or ensure out-of-band access.
3. **Applying PortFast/BPDU Guard on uplinks.** Can block production trunks.
4. **Ignoring stack state.** A failed member changes interface numbering and PoE capacity.
5. **Fixing err-disable without fixing cause.** The port will fail again.
6. **Saving config before validation.** `write memory` only after operational state is confirmed.
7. **LACP mismatch.** Both sides must match LACP/static mode, speed and trunk VLANs.
8. **Zabbix noisy on access ports.** Alert only critical ports unless the user requests exhaustive monitoring.
9. **Pasting full configs.** Sanitize secrets, public IPs, customer names and SNMP communities.

## Report Template

```text
Status: OK / Atenção / Falha
Equipamento: <modelo> <IOS/IOS-XE> <stack?>
Achado: <causa/evidência principal>
Ação: <o que foi feito ou recomendado>
Validação: <show/ping/SNMP/Zabbix>
Próximo passo: <ação objetiva, se houver>
```

## Verification Checklist

- [ ] Model, IOS/IOS-XE version, stack state and management path were identified.
- [ ] Config/snapshot exists before any mutating action.
- [ ] Risky commands were explicitly confirmed.
- [ ] VLAN/trunk/STP/EtherChannel/PoE changes were validated with `show` commands.
- [ ] Management reachability remained available after changes.
- [ ] Zabbix/SNMP checks were run from the actual server/proxy when monitoring was involved.
- [ ] No secrets or sensitive full configs were exposed.
