# LAN scan → Zabbix onboarding workflow

Use when the user asks to scan a local/provider LAN and decide what should be added to Zabbix.

## Goals

- Discover live devices from the Zabbix server/proxy vantage point.
- Classify candidates without immediately polluting Zabbix.
- Prefer safe first-pass monitoring: ICMP for everything, then richer templates for hosts with agent/SNMP.
- Report a concise candidate table and ask before bulk host creation.

## Safe discovery sequence

1. Identify the connected management subnet from the Zabbix host/proxy:

```bash
ip -o -4 addr show scope global
ip route
```

2. Keep scans bounded. For an unknown LAN, start with connected private `/24` networks only; avoid scanning routed/public ranges unless the user explicitly asks.

3. Fast discovery:

```bash
nmap -sn -oX /tmp/ping.xml 10.0.0.0/24
```

4. Scan only live/candidate IPs for infrastructure ports:

```bash
nmap -Pn -sT -T4 --max-retries 1 --host-timeout 12s \
  -p 22,23,53,80,443,8006,8080,8443,8291,8728,8729,10050,10051,3000,9100,161,3306,5432,6379,9090,9443 \
  -oX /tmp/tcp.xml <ip1> <ip2> ...
```

5. Supplement with local ARP/neighbour table and hypervisor inventory when available:

```bash
ip neigh show
pct list
pct config <ctid>
```

6. Probe SNMP conservatively. Test `public` only as a hint; do not assume it is the production community.

```bash
timeout 2 snmpget -v2c -c public -Oqv <ip> 1.3.6.1.2.1.1.1.0
timeout 2 snmpget -v2c -c public -Oqv <ip> 1.3.6.1.2.1.1.5.0
```

## Classification hints

| Evidence | Likely type | First Zabbix action |
|---|---|---|
| `10050/tcp` | Host with Zabbix agent | `Linux by Zabbix agent` / relevant OS template |
| `8006/tcp` | Proxmox node | Linux/Proxmox monitoring; install/configure agent for metrics |
| `8291`, `8728`, `8729`, Routerboard MAC | MikroTik RouterOS | MikroTik by SNMP, after confirming SNMP community |
| `161/udp/tcp` or SNMP sysDescr | SNMP-capable device | Generic/vendor SNMP template |
| `9100/tcp` | Printer/JetDirect-like device | ICMP + printer/SNMP if available |
| only `80/443/8080/8443/3000` | Web/admin service | ICMP + HTTP web scenario/check |
| only ping/ARP | Unknown endpoint/IoT | ICMP Ping first |

## Zabbix workflow

1. Query existing hosts first to avoid duplicates:

```json
{
  "method": "host.get",
  "params": {
    "output": ["hostid", "host", "name"],
    "selectInterfaces": ["ip", "type", "port"]
  }
}
```

2. Produce a candidate report with:

- IP
- detected name/MAC/vendor
- open ports
- guessed device class
- suggested template(s)
- whether already in Zabbix

3. Ask the user which batch to add:

- all with ICMP Ping
- only core infra
- only hosts with agent/SNMP
- configure SNMP first, then add network devices

4. Only create hosts after confirmation. Bulk-add in small batches and validate with `host.get` afterward.

## Pitfalls

- Do not create 40+ hosts immediately after a scan unless the user explicitly approves; it can clutter a fresh Zabbix.
- `nmap -Pn` across a whole `/24` with many ports can be slow; do ping/ARP first, then scan live IPs.
- UDP SNMP scans can hang or run long. Prefer short `snmpget` probes against known live devices.
- `public` SNMP failing does not mean a device cannot be monitored; it usually means SNMP is disabled or uses a different community.
- `api/health` on Grafana only proves the service is alive; use authenticated endpoints such as `/api/user` to verify stored credentials.
