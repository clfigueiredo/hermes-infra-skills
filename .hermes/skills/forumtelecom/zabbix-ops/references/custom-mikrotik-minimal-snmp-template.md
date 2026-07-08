# Custom minimal MikroTik SNMP template (Zabbix 7.x)

Use when the user wants a lightweight MikroTik template instead of the stock `Mikrotik by SNMP` template.

## Goal

Monitor only:

- CPU/processamento
- Interface traffic input/output
- Uptime
- A few practical triggers

Avoid stock template noise such as temperature, storage, wireless/CAPsMAN/LTE discoveries unless requested.

## MikroTik SNMP prep

Before changing RouterOS, identify and export:

```rsc
/system identity print
/system resource print
/snmp print
/snmp community print detail
/export file=pre-zabbix-snmp-YYYYMMDD-HHMMSS
```

Idempotent SNMP v2c community restricted to the Zabbix server:

```rsc
/snmp set enabled=yes contact="Hermes/Zabbix" location="Forum Telecom"
:if ([:len [/snmp community find where name="zbx-hermes"]] = 0) do={
  /snmp community add name="zbx-hermes" addresses=10.0.0.25/32 read-access=yes write-access=no security=none
} else={
  /snmp community set [find where name="zbx-hermes"] addresses=10.0.0.25/32 read-access=yes write-access=no security=none
}
```

Validate from the Zabbix server/container:

```bash
snmpget -v2c -c zbx-hermes -Oqv 10.0.0.169 1.3.6.1.2.1.1.1.0
snmpget -v2c -c zbx-hermes -Oqv 10.0.0.169 1.3.6.1.2.1.1.5.0
```

## Zabbix 7 API pitfalls

- Template groups are managed with `templategroup.get/create`, not `hostgroup.get/create`. Passing a host group id into `template.create.groups` fails with `object does not exist, or you have no permissions to it`.
- `preprocessing` entries must include `error_handler` and `error_handler_params` in Zabbix 7 API calls, e.g. `{'type': 1, 'params': '8', 'error_handler': 0, 'error_handler_params': ''}`.
- `itemprototype.create` requires both `hostid` (template id) and `ruleid`.
- Unlinking/replacing a stock template can leave orphan host-level discovered entities. For a test host where the user explicitly wants only the custom template, delete orphan items/discovery rules with `templateid == 0` after unlinking. Do not do this broadly on production hosts without confirmation.
- After template/link changes, run `zabbix_server -R config_cache_reload` and allow at least one LLD interval before judging item creation.

## Minimal template shape

Template name used in the session:

```text
Template ForumTelecom MikroTik Minimal SNMP
```

Macros:

```text
{$SNMP_COMMUNITY}=zbx-hermes
{$CPU.UTIL.MAX}=85
{$UPTIME.MIN}=600
```

### Fixed item: uptime

```text
name: System uptime
key: system.uptime.network
type: SNMP agent
OID: 1.3.6.1.2.1.1.3.0
value_type: unsigned
units: uptime
preprocessing: multiplier 0.01
```

### CPU discovery

Discovery rule:

```text
name: CPU discovery
key: cpu.discovery
type: SNMP agent
OID: discovery[{#CPU.LOAD},1.3.6.1.2.1.25.3.3.1.2]
```

Item prototype:

```text
name: CPU {#SNMPINDEX}: load
key: cpu.load[{#SNMPINDEX}]
OID: 1.3.6.1.2.1.25.3.3.1.2.{#SNMPINDEX}
units: %
```

Trigger prototype:

```text
CPU alta no core {#SNMPINDEX}
min(/<template>/cpu.load[{#SNMPINDEX}],5m)>{$CPU.UTIL.MAX}
severity: Average
```

### Interface discovery

Discovery rule:

```text
name: Interface discovery
key: net.if.discovery
OID: discovery[{#IFNAME},1.3.6.1.2.1.2.2.1.2,{#IFOPERSTATUS},1.3.6.1.2.1.2.2.1.8]
```

Item prototypes:

```text
Interface {#IFNAME}: entrada
key: if.in[{#SNMPINDEX}]
OID: 1.3.6.1.2.1.31.1.1.1.6.{#SNMPINDEX}
preprocessing: change per second, multiplier 8
units: bps

Interface {#IFNAME}: saída
key: if.out[{#SNMPINDEX}]
OID: 1.3.6.1.2.1.31.1.1.1.10.{#SNMPINDEX}
preprocessing: change per second, multiplier 8
units: bps

Interface {#IFNAME}: status operacional
key: if.operstatus[{#SNMPINDEX}]
OID: 1.3.6.1.2.1.2.2.1.8.{#SNMPINDEX}
```

Do **not** create interface-down triggers by default. MikroTik routers often have unused Ethernet ports down (e.g. ether1/ether5), causing immediate false positives. Add interface-down triggers only for explicitly selected important interfaces.

### Template triggers

```text
MikroTik reboot recente
last(/<template>/system.uptime.network)<{$UPTIME.MIN}
severity: Warning

MikroTik sem coleta SNMP
nodata(/<template>/system.uptime.network,5m)=1
severity: High
```

## Verification

After LLD runs, expected on a hEX/RB750Gr3-like device:

- CPU items: `cpu.load[1]` through `cpu.load[4]`
- Interface items for `lo`, `ether1..ether5`, `bridge1`: `if.in[]`, `if.out[]`, `if.operstatus[]`
- Fixed uptime item has non-empty `lastvalue`
- Host is linked only to the custom template if the user requested no stock MikroTik template
