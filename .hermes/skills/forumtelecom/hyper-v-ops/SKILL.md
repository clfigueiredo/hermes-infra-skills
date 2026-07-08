---
name: hyper-v-ops
description: "Senior Microsoft Hyper-V virtualization engineer for Windows Server and Windows client Hyper-V hosts. Use when the user asks to diagnose, configure, audit, or operate Hyper-V VMs, checkpoints, virtual switches, VLANs, NAT, VHD/VHDX storage, live migration, Replica, Failover Cluster, GPU-P/DDA, or PowerShell remoting. Triggers include Hyper-V, Get-VM, New-VM, Stop-VM, Restart-VM, Checkpoint-VM, VMSwitch, VHDX, Windows Server virtualization, Failover Cluster, Cluster Shared Volumes, Hyper-V Replica, PowerShell Direct, VMConnect, and Windows hypervisor."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux]
metadata:
  hermes:
    tags: [hyper-v, windows-server, virtualization, powershell, infrastructure]
    related_skills: [proxmox-ops, docker-ops]
    source_research:
      - https://github.com/hmohamed01/hyper-v-expert
      - https://github.com/AhmedLaminou/windows-mcp-server
      - https://github.com/SteffenSenchyna/VM-Management
---

# Hyper-V Operations

Senior virtualization engineer for Microsoft Hyper-V. Speak Brazilian Portuguese with the user; keep PowerShell commands and Windows/Hyper-V terminology in original syntax.

This skill is a Hermes-native operational playbook based on Hyper-V PowerShell practices and public GitHub research. It is not a verbatim copy of another agent skill: it adopts the Forum Telecom safety workflow used for network/infra ops.

## Operating posture

Hyper-V changes usually happen over PowerShell Remoting/WinRM, OpenSSH on Windows, or local PowerShell on the host. Prefer **read-only inventory first**, then checkpoint/export/snapshot where applicable, then controlled action, then validation.

For hosts in production, assume VMs may run critical services. Do not force power-off, delete, merge checkpoints, detach disks, change switch/NIC binding, or alter cluster membership without literal confirmation.

## Mandatory workflow

### 1. Identify
Completion criterion: host version, Hyper-V module availability, VM target, storage, and network context are known.

```powershell
$PSVersionTable
Get-ComputerInfo | Select-Object WindowsProductName,WindowsVersion,OsHardwareAbstractionLayer,CsName
Get-WindowsFeature Hyper-V -ErrorAction SilentlyContinue
Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-All -ErrorAction SilentlyContinue
Import-Module Hyper-V
Get-VM | Select-Object Name,State,CPUUsage,MemoryAssigned,Uptime,Status,Version
Get-VMSwitch
Get-VMHost
```

If remote:

```powershell
Test-WSMan <HOST>
Invoke-Command -ComputerName <HOST> -ScriptBlock { Get-VM | Select Name,State }
```

### 2. Snapshot before mutating
Completion criterion: a reversible point exists, or you explicitly explain why no safe snapshot is possible.

For a VM:

```powershell
Set-VM -Name "<VM>" -CheckpointType Production
Checkpoint-VM -Name "<VM>" -SnapshotName "pre-change-$(Get-Date -Format yyyyMMdd-HHmm)"
Get-VMCheckpoint -VMName "<VM>"
```

For high-risk storage work, also export config/details:

```powershell
Get-VM -Name "<VM>" | Format-List *
Get-VMHardDiskDrive -VMName "<VM>" | Format-List *
Get-VHD -Path "<path-to-vhdx>"
```

### 3. Apply cautiously
Completion criterion: only the requested change was applied, with the least disruptive cmdlet.

Prefer graceful operations:

```powershell
Restart-VM -Name "<VM>"              # graceful if integration services support it
Stop-VM -Name "<VM>"                 # graceful shutdown
Start-VM -Name "<VM>"
```

Avoid force unless the user explicitly confirms the impact:

```powershell
Stop-VM -Name "<VM>" -Force
Stop-VM -Name "<VM>" -TurnOff
```

### 4. Validate
Completion criterion: VM/host state proves the requested operation succeeded.

```powershell
Get-VM -Name "<VM>" | Select Name,State,CPUUsage,MemoryAssigned,Uptime,Status
Get-VMIntegrationService -VMName "<VM>"
Get-WinEvent -FilterHashtable @{LogName="Microsoft-Windows-Hyper-V-Worker-Admin"} -MaxEvents 20
```

### 5. Report
Use the report template at the end of this skill.

## Connection patterns

### WinRM / PowerShell Remoting

```powershell
$cred = Get-Credential
Invoke-Command -ComputerName "<HyperVHost>" -Credential $cred -ScriptBlock {
  Import-Module Hyper-V
  Get-VM | Select Name,State,CPUUsage,MemoryAssigned,Uptime
}
```

### OpenSSH on Windows host

If Windows OpenSSH Server is enabled, Hermes can run:

```bash
ssh <user>@<host> "powershell -NoProfile -NonInteractive -Command \"Get-VM | Select Name,State | ConvertTo-Json\""
```

### PowerShell Direct into guest

Only works from the Hyper-V host to supported Windows guests:

```powershell
Enter-PSSession -VMName "<VM>" -Credential (Get-Credential)
Invoke-Command -VMName "<VM>" -Credential $cred -ScriptBlock { hostname; ipconfig }
Copy-VMFile -Name "<VM>" -SourcePath "C:\temp\file.txt" -DestinationPath "C:\temp\file.txt" -CreateFullPath -FileSource Host
```

## Critical commands by domain

### VM lifecycle

```powershell
Get-VM
Get-VM -Name "<VM>" | Format-List *
Start-VM -Name "<VM>"
Stop-VM -Name "<VM>"                 # graceful
Restart-VM -Name "<VM>"
Suspend-VM -Name "<VM>"
Resume-VM -Name "<VM>"
Save-VM -Name "<VM>"
```

Create a modern Gen 2 VM:

```powershell
New-VM -Name "<VM>" -Generation 2 -MemoryStartupBytes 4GB `
  -NewVHDPath "D:\VMs\<VM>\<VM>.vhdx" -NewVHDSizeBytes 80GB `
  -Path "D:\VMs" -SwitchName "<Switch>"
Set-VMProcessor -VMName "<VM>" -Count 2
Set-VMMemory -VMName "<VM>" -DynamicMemoryEnabled $true -MinimumBytes 1GB -StartupBytes 4GB -MaximumBytes 8GB
Add-VMDvdDrive -VMName "<VM>" -Path "D:\ISO\installer.iso"
Set-VMFirmware -VMName "<VM>" -EnableSecureBoot On
```

### Checkpoints

```powershell
Set-VM -Name "<VM>" -CheckpointType Production
Checkpoint-VM -VMName "<VM>" -SnapshotName "BeforeUpdate"
Get-VMCheckpoint -VMName "<VM>"
Restore-VMCheckpoint -VMName "<VM>" -Name "BeforeUpdate" -Confirm:$false
Remove-VMCheckpoint -VMName "<VM>" -Name "BeforeUpdate"
```

Production checkpoints use VSS/fsfreeze and are preferred for production workloads. Standard checkpoints capture memory state and are better suited for labs/testing.

### Networking / switches / VLAN

```powershell
Get-NetAdapter | Where-Object Status -eq "Up"
Get-VMSwitch
New-VMSwitch -Name "External" -NetAdapterName "Ethernet" -AllowManagementOS $true
New-VMSwitch -Name "Internal" -SwitchType Internal
New-VMSwitch -Name "Private" -SwitchType Private
Connect-VMNetworkAdapter -VMName "<VM>" -SwitchName "<Switch>"
Get-VMNetworkAdapter -VMName "<VM>"
Get-VMNetworkAdapterVlan -VMName "<VM>"
Set-VMNetworkAdapterVlan -VMName "<VM>" -Access -VlanId 100
Set-VMNetworkAdapterVlan -VMName "<VM>" -Trunk -NativeVlanId 1 -AllowedVlanIdList "100,200,300"
```

NAT network pattern:

```powershell
New-VMSwitch -Name "NATSwitch" -SwitchType Internal
$ifIndex = (Get-NetAdapter -Name "vEthernet (NATSwitch)").ifIndex
New-NetIPAddress -IPAddress 192.168.100.1 -PrefixLength 24 -InterfaceIndex $ifIndex
New-NetNat -Name "VMNat" -InternalIPInterfaceAddressPrefix "192.168.100.0/24"
Add-NetNatStaticMapping -NatName "VMNat" -Protocol TCP -ExternalIPAddress 0.0.0.0 -ExternalPort 8080 -InternalIPAddress 192.168.100.10 -InternalPort 80
```

For Windows Server 2016+, prefer SET (Switch Embedded Teaming) over legacy LBFO for Hyper-V:

```powershell
New-VMSwitch -Name "SETSwitch" -NetAdapterName "NIC1","NIC2" -EnableEmbeddedTeaming $true
Get-VMSwitchTeam -Name "SETSwitch"
```

### Storage / VHDX

```powershell
Get-VMHardDiskDrive -VMName "<VM>"
Get-VHD -Path "D:\VMs\<VM>\disk.vhdx"
New-VHD -Path "D:\VMs\<VM>\data.vhdx" -SizeBytes 100GB -Dynamic
New-VHD -Path "D:\VMs\<VM>\data-fixed.vhdx" -SizeBytes 100GB -Fixed
Add-VMHardDiskDrive -VMName "<VM>" -Path "D:\VMs\<VM>\data.vhdx"
Resize-VHD -Path "D:\VMs\<VM>\disk.vhdx" -SizeBytes 200GB
Optimize-VHD -Path "D:\VMs\<VM>\disk.vhdx" -Mode Full
Convert-VHD -Path "D:\old.vhd" -DestinationPath "D:\new.vhdx"
```

Rules of thumb:
- Use **VHDX** for modern guests; VHD is legacy and capped at 2 TB.
- Use fixed VHDX for performance-critical workloads.
- Dynamic VHDX is fine for general-purpose servers when storage is monitored.
- For guest clusters, use VHD Set (`.vhds`) where supported.

### Export / import / clone

```powershell
Export-VM -Name "<VM>" -Path "D:\Exports"
Import-VM -Path "D:\Exports\<VM>\Virtual Machines\*.vmcx"
Import-VM -Path "D:\Exports\<VM>\Virtual Machines\*.vmcx" -Copy -GenerateNewId
```

### Live migration / storage migration

```powershell
Enable-VMMigration
Set-VMMigrationNetwork 192.168.1.0/24
Set-VMHost -VirtualMachineMigrationAuthenticationType Kerberos
Move-VM -Name "<VM>" -DestinationHost "<DestHost>"
Move-VM -Name "<VM>" -DestinationHost "<DestHost>" -DestinationStoragePath "D:\VMs"
Move-VMStorage -VMName "<VM>" -DestinationStoragePath "E:\VMs"
```

Before live migration verify:
- compatible host versions;
- same virtual switch names or a mapping plan;
- authentication/delegation configured;
- storage reachable and enough bandwidth.

### Failover Cluster / CSV

```powershell
Get-Cluster
Get-ClusterNode
Get-ClusterGroup
Get-ClusterSharedVolume
Get-ClusterResource
Get-ClusterGroup -Name "<VMGroup>" | Move-ClusterVirtualMachineRole -Node "<TargetNode>"
```

### Hyper-V Replica

Replica health:

```powershell
Get-VMReplication -VMName "<VM>"
Measure-VMReplication -VMName "<VM>"
Resume-VMReplication -VMName "<VM>" -Resynchronize
```

Enable replica server and VM replication:

```powershell
Set-VMReplicationServer -ReplicationEnabled $true -AllowedAuthenticationType Kerberos -DefaultStorageLocation "D:\Replicas"
Enable-VMReplication -VMName "<VM>" -ReplicaServerName "ReplicaHost.domain.local" -ReplicaServerPort 80 -AuthenticationType Kerberos
Start-VMInitialReplication -VMName "<VM>"
```

### Monitoring / health

```powershell
Get-VM | Select Name,State,CPUUsage,MemoryAssigned,Uptime,Status
Enable-VMResourceMetering -VMName "<VM>"
Measure-VM -VMName "<VM>"
Reset-VMResourceMetering -VMName "<VM>"
Get-VMIntegrationService -VMName "<VM>"
Get-WinEvent -FilterHashTable @{LogName="Microsoft-Windows-Hyper-V-Worker-Admin"} -MaxEvents 20
Get-WinEvent -FilterHashTable @{LogName="Microsoft-Windows-Hyper-V-VMMS-Admin"} -MaxEvents 20
```

## Decision points

### VM generation

```text
Legacy OS, 32-bit, BIOS-only, old PXE, or Windows Server 2003/XP? → Generation 1
Modern Windows/Linux x64 with UEFI support? → Generation 2
Need Secure Boot/vTPM? → Generation 2
```

### Checkpoint type

```text
Production server? → Production checkpoint
Lab/test rollback? → Standard checkpoint acceptable
Application cannot tolerate snapshot quiescing? → Prefer backup/export/maintenance window
```

### Stop method

```text
Guest responsive and integration services healthy? → Stop-VM / Restart-VM
Guest hung but service impact accepted? → ask for CONFIRMO before Stop-VM -Force
Data corruption risk acceptable only in emergency? → ask for CONFIRMO before -TurnOff
```

## Safety rules

### NEVER without literal confirmation
- `Remove-VM`
- deleting VHD/VHDX files with `Remove-Item`
- `Stop-VM -Force` or `Stop-VM -TurnOff` on production workloads
- `Restore-VMCheckpoint` on production workloads
- `Remove-VMCheckpoint` when checkpoints may still be needed for rollback
- `Remove-VMSwitch`, especially external switch bound to management NIC
- changing VLAN/trunk on management or production NICs
- `Move-ClusterGroup`, `Move-ClusterVirtualMachineRole`, `Remove-ClusterNode`
- enabling/disabling Replica failover
- resizing/compacting disks without storage and guest filesystem plan

Confirmation pattern:

> Operação perigosa: `<comando>`
> Impacto: <risco em uma frase>
> Para executar, responda exatamente: `CONFIRMO <comando>`

Do not accept "sim", "pode", "manda", or paraphrases.

### ALWAYS warn before
- changing an external switch or NIC team on a remote host;
- live migrating large VMs during business hours;
- creating checkpoints on heavy I/O production workloads;
- expanding VHDX without confirming guest partition/filesystem expansion;
- running scripts from GitHub or unknown sources on Windows hosts.

## Typical provider/MSP tasks

| Pedido | Safe first action |
|---|---|
| "lista as VMs do Hyper-V" | `Get-VM | Select Name,State,CPUUsage,MemoryAssigned,Uptime` |
| "reinicia a VM X" | `Get-VM X`; checkpoint if appropriate; `Restart-VM X`; validate |
| "cria uma VM Windows" | validate switch/storage/ISO, then `New-VM` + `Add-VMDvdDrive` |
| "libera VLAN 200 na VM" | snapshot config, `Get-VMNetworkAdapterVlan`, then `Set-VMNetworkAdapterVlan` |
| "a VM não sobe" | inspect `Get-VM`, event logs, VHD path, switch, integration status |
| "mover VM para outro host" | validate live migration prerequisites and storage/switch mapping |
| "limpar checkpoints" | list tree first; confirm removal; monitor merge progress |

## Troubleshooting recipes

### VM will not start

```powershell
Get-VM -Name "<VM>" | Format-List *
Get-VMHardDiskDrive -VMName "<VM>" | Format-List *
Get-VMNetworkAdapter -VMName "<VM>"
Get-WinEvent -FilterHashTable @{LogName="Microsoft-Windows-Hyper-V-Worker-Admin"} -MaxEvents 50
Get-WinEvent -FilterHashTable @{LogName="Microsoft-Windows-Hyper-V-VMMS-Admin"} -MaxEvents 50
```

Check for missing VHDX, invalid switch, insufficient memory, saved state corruption, checkpoint merge in progress, or permissions on VM files.

### VM network issue

```powershell
Get-VMNetworkAdapter -VMName "<VM>" | Format-List *
Get-VMNetworkAdapterVlan -VMName "<VM>"
Get-VMSwitch | Format-List *
Get-NetAdapter | Select Name,Status,LinkSpeed,MacAddress
Test-NetConnection <VM-IP>
```

### Storage pressure

```powershell
Get-Volume
Get-VM | Get-VMHardDiskDrive | Select VMName,Path
Get-ChildItem D:\VMs -Recurse -Include *.vhd,*.vhdx,*.avhdx | Sort-Object Length -Descending | Select FullName,Length -First 20
```

`.avhdx` files indicate checkpoints/differencing disks. Do **not** delete manually.

## Report template

```markdown
## Operação Hyper-V: <título>
**Host:** <hostname/IP>
**VM/Objeto:** <VM/switch/storage/cluster>

**Comandos executados:**
- `<cmd>` → <resultado resumido>

**Estado antes:**
- ...

**Estado depois:**
- ...

**Análise:**
<2-5 linhas objetivas>

**Rollback:**
```powershell
<comandos se aplicável>
```

**Próximos passos:**
- ...
```

## When NOT to use

- Proxmox, VMware ESXi/vCenter, KVM/libvirt, or Docker operations — use the appropriate skill.
- Physical Windows Server tasks unrelated to Hyper-V unless they directly affect the virtualization host.
- Password recovery or bypassing Windows/AD security.
