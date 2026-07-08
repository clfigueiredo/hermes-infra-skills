---
name: vmware-ops
description: "Senior VMware vSphere/vCenter/ESXi virtualization engineer for ISP/MSP and datacenter operations. Use when the user asks to diagnose, audit, configure, or operate VMware environments via vCenter REST API, VI/JSON, SOAP/pyVmomi, PowerCLI, ESXi SSH/esxcli, or web-GUI guidance: VMs, templates, snapshots, hosts, clusters, DRS/HA, datastores, vSAN, networks, port groups, distributed switches, vMotion, Storage vMotion, alarms, events, tasks, performance, VMware Tools, ISO/media, RBAC, permissions, lifecycle/vLCM, maintenance mode, and troubleshooting VM/host/storage/network issues. Triggers include VMware, vSphere, vCenter, ESXi, VMFS, datastore, snapshot, vMotion, DRS, HA, vSAN, PowerCLI, pyVmomi."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, windows, vmware-esxi]
metadata:
  hermes:
    tags: [vmware, vsphere, vcenter, esxi, virtualization, datacenter, powercli, pyvmomi]
    related_skills: [proxmox-ops, hyper-v-ops]
    source_research:
      - https://github.com/TheEvalon/vmware-vcenter-mcp
      - https://github.com/giuliolibrando/vmware-vsphere-mcp-server
      - https://github.com/bright8192/esxi-mcp-server
      - https://github.com/adrianlizman/vmware-mcp-server
      - https://github.com/vmware/pyvmomi-community-samples
---

# VMware vSphere / vCenter / ESXi Operations

Senior VMware virtualization engineer for production vSphere environments. Speak Brazilian Portuguese with the user; keep VMware object names, API paths, PowerCLI cmdlets, `govc`, `esxcli`, and ESXi/vCenter terminology in original syntax.

This is a Hermes-native operational playbook based on public VMware/vSphere MCP servers, pyVmomi community samples, and production VMware safety patterns. It is not copied verbatim from another agent skill. It follows the Forum Telecom model: **Identify → Snapshot → Apply → Validate → Report**.

## Operating posture

Prefer this order:

1. **vCenter API / PowerCLI / govc / pyVmomi** for structured inventory and normal operations.
2. **vCenter tasks/events/alarms** for verification and audit trail.
3. **ESXi SSH / `esxcli`** only for host-local diagnostics or when vCenter is unavailable.
4. **Web GUI guidance** for actions that are version/plugin-specific or too risky to automate blindly.

Strong public patterns found in VMware MCP projects:
- read-only mode first;
- destructive tools require explicit `confirm` / dry-run preview;
- global kill switch like `VCENTER_READ_ONLY=true`;
- credentials only from environment variables or a secure secret manager, never hardcoded;
- long-running operations are tasks and must be polled to terminal state;
- vCenter 8 may require multiple API surfaces: REST `/api`, VI/JSON `/sdk/vim25/...`, SOAP/pyVmomi fallback.

## Connection variables

Typical connection fields:

| Variable | Purpose |
|---|---|
| `VCENTER_HOST` | vCenter hostname/IP, no scheme unless tool requires URL |
| `VCENTER_PORT` | usually `443` |
| `VCENTER_USER` | e.g. `administrator@vsphere.local` or AD user |
| `VCENTER_PASS` / password | vCenter password from a secure source |
| `VCENTER_INSECURE` | `true` only for self-signed/homelab certs |
| `VCENTER_READ_ONLY` | set `true` for audit/discovery-only sessions |
| `ESXI_HOST` | direct host access when no vCenter exists |
| `ESXI_USER`, `ESXI_PASS` | ESXi SSH/API credentials |

Do not print passwords, session IDs, cookies, VMRC console tickets, API tokens, or complete support bundles in chat.

## Mandatory workflow

### 1. Identify
Completion criterion: target vCenter/ESXi, datacenter/cluster/host, object MoRef/name/UUID, current state, and risk class are known.

PowerCLI probes:

```powershell
Connect-VIServer -Server $env:VCENTER_HOST -User $env:VCENTER_USER -Password $env:VCENTER_PASS
Get-View ServiceInstance | Select-Object -ExpandProperty Content
Get-Datacenter
Get-Cluster
Get-VMHost | Select Name,ConnectionState,PowerState,Version,Build
Get-VM | Select Name,PowerState,VMHost,NumCpu,MemoryGB
Get-Datastore | Select Name,Type,CapacityGB,FreeSpaceGB
Get-Task | Sort StartTime -Descending | Select -First 20
Get-AlarmDefinition | Select -First 20
```

`govc` probes:

```bash
export GOVC_URL="https://$VCENTER_HOST/sdk"
export GOVC_USERNAME="$VCENTER_USER"
export GOVC_PASSWORD="$VCENTER_PASS"
export GOVC_INSECURE=true   # only for self-signed/internal certs

govc about
govc datacenter.info
govc ls
govc find / -type m
govc host.info
govc datastore.info
govc events -n 20
```

ESXi SSH probes:

```sh
vmware -v
hostname
esxcli system version get
esxcli system maintenanceMode get
esxcli network ip interface list
esxcli network nic list
esxcli storage filesystem list
vim-cmd vmsvc/getallvms
```

### 2. Snapshot before mutating
Completion criterion: rollback path exists or current state is recorded.

For VM changes:

```powershell
Get-VM -Name '<vm>' | Select Name,PowerState,VMHost,NumCpu,MemoryGB,Folder | Format-List
Get-Snapshot -VM '<vm>'
New-Snapshot -VM '<vm>' -Name 'pre-hermes-change' -Description 'Before change requested via Hermes' -Quiesce:$false -Memory:$false
```

Do **not** create snapshots blindly for every operation. Avoid snapshots on huge/high-I/O databases unless the user accepts risk. Prefer application-aware backup/checkpoint when needed.

For host/cluster/network/storage changes:

```powershell
Get-VMHost '<host>' | Format-List *
Get-VirtualSwitch -VMHost '<host>'
Get-VirtualPortGroup -VMHost '<host>'
Get-Datastore | Sort FreeSpaceGB
Get-Cluster | Select Name,DrsEnabled,HAEnabled
```

For ESXi host config backup:

```sh
vim-cmd hostsvc/firmware/sync_config
vim-cmd hostsvc/firmware/backup_config
```

### 3. Apply cautiously
Completion criterion: smallest requested delta is submitted as a tracked task, not a broad implicit change.

VM lifecycle:

```powershell
Start-VM -VM '<vm>'
Restart-VMGuest -VM '<vm>' -Confirm:$false     # guest-aware reboot when Tools healthy
Restart-VM -VM '<vm>' -Confirm:$false          # reset/power cycle; higher impact
Stop-VMGuest -VM '<vm>' -Confirm:$false
Stop-VM -VM '<vm>' -Confirm:$false             # hard power off; dangerous
```

Snapshots:

```powershell
Get-Snapshot -VM '<vm>'
New-Snapshot -VM '<vm>' -Name '<name>' -Description '<why>' -Memory:$false -Quiesce:$false
Remove-Snapshot -Snapshot '<snapshot>' -Confirm:$false
Set-VM -VM '<vm>' -Snapshot '<snapshot>' -Confirm:$false   # revert; dangerous
```

Resources:

```powershell
Set-VM -VM '<vm>' -NumCpu 4 -MemoryGB 8 -Confirm:$false
Move-VM -VM '<vm>' -Destination '<host-or-cluster>'
Move-VM -VM '<vm>' -Datastore '<datastore>'
```

Networks:

```powershell
Get-NetworkAdapter -VM '<vm>'
Set-NetworkAdapter -NetworkAdapter '<nic>' -NetworkName '<portgroup>' -Confirm:$false
Get-VirtualPortGroup
Get-VDPortgroup
```

Host maintenance:

```powershell
Set-VMHost -VMHost '<host>' -State Maintenance
Set-VMHost -VMHost '<host>' -State Connected
```

### 4. Validate
Completion criterion: object state, task state, events, and dependent service checks prove the operation succeeded.

```powershell
Get-Task | Sort StartTime -Descending | Select -First 10 Name,State,PercentComplete,StartTime,FinishTime
Get-VM -Name '<vm>' | Select Name,PowerState,VMHost,NumCpu,MemoryGB
Get-VMQuestion -VM '<vm>'
Get-VMGuest -VM '<vm>'
Get-Snapshot -VM '<vm>'
Get-Event -Entity '<vm>' -MaxSamples 20
Get-AlarmAction -AlarmDefinition * 2>$null
```

ESXi validation:

```sh
vim-cmd vmsvc/power.getstate <vmid>
vim-cmd vmsvc/get.summary <vmid>
esxcli vm process list
esxcli storage filesystem list
esxcli network vm list
```

### 5. Report
Use the report template at the end. Include task IDs/results and summarized state; never include secrets.

## API / tool surface quick reference

### vCenter REST / VI/JSON

Modern vCenter operations may use:

```text
POST /api/session
GET  /api/vcenter/vm
GET  /api/vcenter/host
GET  /api/vcenter/datastore
GET  /api/vcenter/network
GET  /api/vcenter/cluster
POST /api/vcenter/vm/<vm>/power/start
POST /api/vcenter/vm/<vm>/power/stop
POST /api/vcenter/vm/<vm>/power/reset
```

vCenter 8.0 U1+ VI/JSON exposes deeper vim25 operations:

```text
/sdk/vim25/{release}/...
```

Use VI/JSON or pyVmomi for snapshots, performance counters, alarms, RBAC, and advanced VM/host configuration not exposed by REST.

### pyVmomi useful sample categories

The official community samples include patterns for:
- `getallvms.py`, `vminfo_quick.py`, `getvmsbycluster.py`;
- `create_snapshot.py`, `snapshot_operations.py`, `reboot_vm.py`, `soft_reboot.py`;
- `clone_vm.py`, `relocate_vm.py`, `vm_power_on.py`;
- `list_datastore_info.py`, `get_portgroup.py`, `list_vlan_in_portgroups.py`;
- `list_vmwaretools_status.py`, `list_host_alarms.py`;
- `vsan-samples/*` for vSAN health/capacity workflows.

### ESXi SSH / esxcli quick reference

Read-only diagnostics:

```sh
esxcli system version get
esxcli hardware platform get
esxcli system uptime get
esxcli system maintenanceMode get
esxcli system syslog config get
esxcli vm process list
esxcli storage core device list
esxcli storage filesystem list
esxcli network nic list
esxcli network vswitch standard list
esxcli network vswitch dvs vmware list
esxcli network ip route ipv4 list
esxtop -b -n 1
```

VM local commands:

```sh
vim-cmd vmsvc/getallvms
vim-cmd vmsvc/power.getstate <vmid>
vim-cmd vmsvc/power.on <vmid>
vim-cmd vmsvc/power.shutdown <vmid>
vim-cmd vmsvc/power.reboot <vmid>
vim-cmd vmsvc/power.reset <vmid>
```

Use direct ESXi commands only when vCenter is unavailable or user explicitly wants host-local action.

## Common operational recipes

### VM will not power on

1. Identify VM, host, datastore, last task/event.
2. Check datastore free space and file locks.
3. Check VM question and snapshots.
4. Check host state and HA/DRS alarms.
5. Validate after remediation.

```powershell
Get-VM '<vm>' | Format-List *
Get-VMQuestion -VM '<vm>'
Get-Snapshot -VM '<vm>'
Get-Datastore | Sort FreeSpaceGB
Get-Event -Entity (Get-VM '<vm>') -MaxSamples 50
```

Host-local lock check:

```sh
vmkfstools -D /vmfs/volumes/<datastore>/<vm>/<disk>.vmdk
esxcli vm process list
```

### Snapshot sprawl / datastore filling

1. List snapshots and age/size where available.
2. Check datastore free space before consolidation/removal.
3. Prefer consolidation during low I/O windows.
4. Validate `ConsolidationNeeded` and task completion.

```powershell
Get-VM | Get-Snapshot | Select VM,Name,Created,SizeGB,Description
Get-VM | Where-Object {$_.ExtensionData.Runtime.ConsolidationNeeded -eq $true}
Get-Datastore | Select Name,FreeSpaceGB,CapacityGB
```

### Reboot a VM safely

1. Confirm target identity and guest OS.
2. Prefer guest-aware reboot when VMware Tools is running.
3. Snapshot first only when requested/appropriate.
4. Poll power state/tools/heartbeat after reboot.

```powershell
Get-VM '<vm>' | Select Name,PowerState
Get-VMGuest '<vm>'
Restart-VMGuest -VM '<vm>' -Confirm:$false
Start-Sleep 30
Get-VMGuest '<vm>'
```

If guest tools are unhealthy, ask before `Restart-VM` reset.

### Put ESXi host into maintenance

1. Confirm cluster/DRS/HA status and evacuation capacity.
2. Check running VMs and datastore accessibility.
3. Migrate or shut down VMs according to policy.
4. Enter maintenance and validate host state.

```powershell
Get-VMHost '<host>' | Get-VM
Get-Cluster '<cluster>' | Select DrsEnabled,HAEnabled
Set-VMHost -VMHost '<host>' -State Maintenance
Get-VMHost '<host>' | Select Name,ConnectionState
```

### Datastore capacity issue

```powershell
Get-Datastore | Sort FreeSpaceGB | Select Name,Type,CapacityGB,FreeSpaceGB
Get-VM | Get-Snapshot | Sort Created
Get-VM | Where-Object {$_.ExtensionData.Runtime.ConsolidationNeeded -eq $true}
```

Check ISO/temp files before deleting anything. Deleting datastore files requires confirmation.

### Network / VLAN issue

```powershell
Get-VM '<vm>' | Get-NetworkAdapter
Get-VirtualPortGroup | Select Name,VirtualSwitch,VLanId
Get-VDPortgroup | Select Name,VlanConfiguration
Get-VMHostNetworkAdapter -VMHost '<host>'
```

On ESXi:

```sh
esxcli network nic list
esxcli network vswitch standard portgroup list
esxcli network vswitch dvs vmware list
esxcli network ip interface list
```

## Safety rules

### NEVER without literal confirmation
- delete/destroy VM, template, folder, datacenter, resource pool;
- delete or move datastore files/VMDK/VMX/ISO;
- hard power off/reset/suspend production VM;
- revert snapshot, remove all snapshots, consolidate snapshots on high-I/O VM;
- remove host from vCenter, disconnect host, reboot/shutdown ESXi host;
- enter maintenance mode on production host if evacuation capacity is unknown;
- change management vmkernel network, vSwitch/dvSwitch uplinks, VLANs, MTU, LACP/teaming;
- change DRS/HA/vSAN/vLCM/remediation settings;
- assign RBAC permissions or mint console tickets;
- run `esxcli system shutdown/reboot`;
- manipulate `.vmx`/`.vmdk` files directly.

Confirmation pattern:

> Operação perigosa: `<ação/comando>`
> Impacto: <risco em uma frase>
> Para executar, responda exatamente: `CONFIRMO <ação/comando>`

Do not accept “sim”, “pode”, “manda”, or paraphrases.

### ALWAYS warn before
- operations that create vCenter tasks lasting minutes/hours: clone, deploy OVA/OVF, vMotion, Storage vMotion, vLCM remediation;
- snapshots on database/file-server/high-I/O VMs;
- host maintenance where DRS/HA may move customer workloads;
- network changes affecting management, storage, vMotion, or customer VLANs;
- using `VCENTER_INSECURE=true` outside trusted internal networks;
- direct ESXi operation when vCenter is healthy.

## Manual/API-limited operations

Prefer GUI guidance unless the exact API/tooling has been tested for that environment:
- complex vDS/LACP/uplink remaps;
- vSAN disk group rebuild/remediation;
- certificate replacement and SSO identity source changes;
- NSX integrations;
- VCSA patch/upgrade and backup/restore;
- SRM and backup product workflows.

## Report template

```markdown
## Operação VMware: <título>
**vCenter/ESXi:** <hostname/IP>
**Objeto:** <VM/host/datastore/network/cluster>

**Comandos/API usados:**
- `<cmd ou endpoint>` → <resultado resumido>

**Estado antes:**
- ...

**Estado depois:**
- ...

**Tarefas/eventos:**
- Task/Event ID: ... → ...

**Análise:**
<2-5 linhas objetivas>

**Rollback:**
```powershell
<comandos ou caminho GUI/API se aplicável>
```

**Próximos passos:**
- ...
```

## When NOT to use

- Proxmox, Hyper-V, Docker, OPNsense, MikroTik, Cisco, Huawei, Zabbix — use the specific skill.
- Password recovery/bypass, license circumvention, or disabling security/audit controls.
