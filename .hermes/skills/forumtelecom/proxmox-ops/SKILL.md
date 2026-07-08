---
name: proxmox-ops
description: Senior Proxmox VE engineer for cluster management, VM/CT operations, storage, networking, and backup. Use when the user asks to create, diagnose, migrate, or troubleshoot KVM VMs (qm) or LXC containers (pct) on Proxmox VE. Triggers include Proxmox, PVE, Proxmox VE, qm, pct, pvesh, pvesm, pveceph, "proxmox cluster", "create vm proxmox", "lxc container", "proxmox backup", "vzdump", "ceph proxmox", "zfs proxmox".
metadata: { "openclaw": { "emoji": "🖥️", "requires": { "anyBins": ["ssh"], "env": ["PVE_HOST"] } } }
---

# Proxmox VE Operations

Senior virtualization engineer for Proxmox VE clusters. Speak Brazilian Portuguese, use Proxmox CLI (`qm`, `pct`, `pvesh`, `pvesm`).

## Platform context

Proxmox VE is a Debian-based hypervisor with two workload types:
- **VMs (KVM)**: managed by `qm` command
- **CT (LXC containers)**: managed by `pct` command

Cluster operations use `pvecm`. Storage is `pvesm`. API is `pvesh`. All command output is also available via web UI on port 8006.

## Mandatory workflow

### 1. Identify cluster state
```bash
pveversion
pvecm status                    # cluster health
pvesh get /nodes
pvesh get /cluster/resources --type vm
```

### 2. Snapshot before mutating
For VMs:
```bash
qm snapshot <VMID> pre-change --description "Before <change>"
```
For CTs:
```bash
pct snapshot <CTID> pre-change --description "Before <change>"
```

### 3. Apply with caution
- Avoid destructive ops without confirmation
- For migrations, prefer `online` (live) when possible
- For storage changes, check `df -h` and `pvesm status` first

### 4. Validate
```bash
qm status <VMID>
pct status <CTID>
```

### 5. Report.

## Connection

| Variable | Default | Purpose |
|---|---|---|
| `PVE_HOST` | — | required (any cluster node) |
| `PVE_USER` | `root@pam` | API user |
| `PVE_TOKEN_ID` / `PVE_TOKEN_SECRET` | — | API token (preferred over password) |

Via SSH (mais comum):
```bash
ssh root@${PVE_HOST} "qm list"
```

Via API (curl):
```bash
curl -k -H "Authorization: PVEAPIToken=${PVE_USER}!${PVE_TOKEN_ID}=${PVE_TOKEN_SECRET}" \
  https://${PVE_HOST}:8006/api2/json/nodes
```

## Critical commands

### Cluster
```bash
pvecm status
pvecm nodes
pvesh get /cluster/status
pvesh get /cluster/resources
ha-manager status                 # se HA configurado
corosync-cfgtool -s              # estado do corosync
```

### VMs (KVM)
```bash
qm list                          # listar todas
qm status <VMID>
qm config <VMID>
qm start <VMID>
qm shutdown <VMID>               # graceful (ACPI)
qm stop <VMID>                   # force kill (cuidado)
qm reset <VMID>                  # reset (cuidado)
qm reboot <VMID>                 # graceful reboot
qm migrate <VMID> <target-node> --online    # live migration
qm clone <VMID> <NEW_VMID> --full --name new-vm
qm destroy <VMID> --purge        # PERIGOSO
```

### Containers (LXC)
```bash
pct list
pct status <CTID>
pct config <CTID>
pct start <CTID>
pct stop <CTID>
pct exec <CTID> -- <comando>     # executar comando dentro
pct enter <CTID>                 # shell interativo
pct migrate <CTID> <target>
pct clone <CTID> <NEW_CTID>
pct destroy <CTID>               # PERIGOSO
```

### Storage
```bash
pvesm status                     # todos storages
pvesm list <storage_id>          # conteúdo
df -h                            # storage local
zpool status                     # ZFS
zfs list
ceph status                      # se Ceph
ceph df
```

### Backup (vzdump)
```bash
# Backup manual
vzdump <VMID> --storage local --mode snapshot --compress zstd

# Listar backups
pvesm list <backup_storage_id>

# Restaurar VM
qmrestore /var/lib/vz/dump/vzdump-qemu-100-2026_04_29-03_00_00.vma.zst 200 --storage local-lvm

# Restaurar CT
pct restore 200 /var/lib/vz/dump/vzdump-lxc-100-2026_04_29-03_00_00.tar.zst --storage local-lvm
```

### Network
```bash
ip a
brctl show                       # bridges Linux (vmbr*)
cat /etc/network/interfaces
pvesh get /nodes/<node>/network  # via API
```

### Logs
```bash
journalctl -u pve-cluster -f
journalctl -u pveproxy -f
journalctl -u qmeventd
tail -f /var/log/pveproxy/access.log
tail -f /var/log/syslog
```

For deeper VM/CT operations see `references/vm-ct-operations.md`.
For cluster troubleshooting see `references/cluster-troubleshooting.md`.
For a fresh Zabbix + Grafana LXC build from zero, see `references/fresh-zabbix-grafana-lxc.md`.

## Safety rules

### NEVER without confirmation
- `qm destroy` (apaga VM)
- `pct destroy` (apaga CT)
- `pvesm remove <storage>` (remove storage)
- `pvecm delnode` (remove nó do cluster)
- `qm stop` em VM crítica (force kill)
- `rm -rf /var/lib/vz/...` (apaga dados)
- `pveceph purge` (apaga cluster Ceph)

### ALWAYS warn before
- Live migration de VM grande em horário comercial (impacto de rede)
- `qm reset` (não graceful)
- Reboot de nó com VMs sem HA configurado
- Aumentar disco mas não expandir filesystem dentro

### User intent pitfall: “criar do zero” vs reutilizar
- Quando o usuário pedir para **criar/subir um container novo/do zero**, não reutilize CTs existentes só porque têm nome parecido ou stack parecida.
- Primeiro descubra CTID/IP livres, crie um LXC novo com `pct create`, instale a stack nele e valide do zero.
- Só reaproveite um CT existente quando o usuário pedir explicitamente para corrigir, completar ou usar aquele CT.

### Confirmation pattern
> Operação perigosa: `<comando>`
> Impacto: <quantas VMs/CTs ou clientes afetados>
> Para executar, responda: `CONFIRMO <comando>`

## Casos típicos de provedor (deep)

### Hospedagem de serviços críticos do provedor

Provedor típico roda em Proxmox a stack interna toda: sistema de gestão (IXC, Hubsoft, MK-Auth), portal cliente, RADIUS, looking glass, Zabbix, DNS recursivo. Arquitetura padrão:

- **3 nodes em cluster** com Ceph RBD ou ZFS replicado
- **Network bonding LACP** (2x 10G) para storage + (2x 1G) para corosync isolado
- **VLANs separadas**: gerência, storage, produção, cluster heartbeat
- **PBS (Proxmox Backup Server)** dedicado para retention de 30+ dias

### Cluster 3-node com HA real

```bash
# Node 1 cria
pvecm create CLUSTER-PROD --link0 10.0.10.1 --link1 10.0.20.1

# Nodes 2 e 3 entram
pvecm add 10.0.10.1 --link0 10.0.10.2 --link1 10.0.20.2

# Verificar quorum
pvecm status
```

`--link0` e `--link1` são **redes redundantes** para corosync. Sem isso, qualquer hiccup de rede causa fence indevido. Em provedor isso é **obrigatório**.

### HA group + auto-failover de VM

```bash
ha-manager add vm:101 --group critical-services --max_restart 3 --max_relocate 1
```

Configurar HA no GUI: Datacenter > HA > Groups. Restricted=true previne migração para nodes fora do grupo.

### Replicação ZFS (alternativa ao Ceph para clusters menores)

Para clusters 2-3 nodes sem stack Ceph completa:

```bash
pvesr create-local-job 101-0 <target-node> --schedule "*/15"
pvesr status
pvesr run --id 101-0
```

Replica a cada 15min. Failover é manual mas rápido (segundos).

### Backup com PBS + retenção

```bash
# No PVE, adicionar PBS como storage
pvesm add pbs pbs-prod --server pbs.lan --datastore prod-backups \
  --username root@pam --fingerprint <SHA256>

# Job automático
pvesh create /cluster/backup --vmid 101,102,103 --storage pbs-prod \
  --schedule "0 2 * * *" --mode snapshot --compress zstd
```

PBS faz **deduplicação** real — backup full diário ocupa pouco espaço incremental.

### Templates para provisionamento rápido

Padrão: criar uma VM "golden" (debian12-template), instalar tudo, converter em template. Depois clones linkados são instantâneos:

```bash
qm clone 9000 105 --name vm-novo-cliente --full 0   # linked clone
qm set 105 --ipconfig0 ip=10.0.0.105/24,gw=10.0.0.1
qm start 105
```

### Operações típicas via WhatsApp (NetAgent)

| Pedido | Ação |
|---|---|
| "Como tá o cluster?" | `pvecm status` + `pvesh get /cluster/resources` |
| "VM do IXC tá lenta" | `qm config <id>` + `pvesh get /nodes/<n>/stats` |
| "Restaurar backup de ontem" | listar `pvesm list pbs-prod --content backup` + `qmrestore` |
| "Snapshot antes do upgrade" | `qm snapshot <id> pre-upgrade` |
| "Quanto storage livre?" | `pvesm status` |

## Report template

```markdown
## Operação: <título>
**Cluster:** <nome ou IP>
**Workload:** VM 101 / CT 205 / Storage local-zfs

**Comandos:**
- `<cmd>` → <resultado resumido>

**Estado antes:**
- ...

**Estado depois:**
- ...

**Próximos passos:** <bullets>
**Rollback:** `<comandos>`
```
