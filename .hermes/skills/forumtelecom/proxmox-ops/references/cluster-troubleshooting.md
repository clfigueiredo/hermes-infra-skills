# Proxmox cluster — troubleshooting

## Estado saudável de um cluster

```bash
pvecm status
```

Saída esperada:
```
Cluster information
-------------------
Name:             my-cluster
Config Version:   3
Transport:        knet
Secure auth:      on

Quorum information
------------------
Date:             ...
Quorum provider:  corosync_votequorum
Nodes:            3
Node ID:          0x00000001
Ring ID:          1.5
Quorate:          Yes

Votequorum information
----------------------
Expected votes:   3
Highest expected: 3
Total votes:      3
Quorum:           2
Flags:            Quorate
```

`Quorate: Yes` = cluster saudável.

## Problemas comuns

### 1. "No quorum" / cluster fora do quorum

Causa: maioria dos nós perdeu comunicação corosync.

Verificar:
```bash
corosync-cfgtool -s
corosync-quorumtool -s
journalctl -u corosync -n 100
```

Soluções:
- Verificar conectividade de rede entre nós (idealmente em rede dedicada de cluster)
- `pvecm expected 1` em emergência (cluster volta a aceitar config local — só faz se você tem 1 nó vivo e precisa operar)
- Reiniciar corosync: `systemctl restart corosync && systemctl restart pve-cluster`

### 2. "TASK ERROR: connection timed out"

Geralmente quando um nó está offline mas não foi removido do cluster.

```bash
pvesh get /cluster/resources --type node
# se nó X aparece como offline há tempo, ou removê-lo:
pvecm delnode <nome-do-nó>
# OU traze-lo de volta corrigindo network
```

### 3. Storage offline (LVM, NFS, Ceph)

```bash
pvesm status
# se algum storage está "inactive", investigar:

# LVM
vgs
lvs
pvs

# NFS
showmount -e <nfs-server>
mount | grep nfs

# Ceph
ceph -s
ceph osd tree
```

### 4. VM stuck / não inicia

```bash
# Ver lock
qm config <VMID> | grep lock

# Forçar unlock
qm unlock <VMID>

# Ver logs
journalctl -u qemu-server@<VMID> -n 50

# Verificar se processo qemu está vivo
ps aux | grep "id=<VMID>"
```

### 5. HA (High Availability) não está fazendo failover

```bash
ha-manager status
ha-manager config

# Ver fence devices
pvesh get /cluster/ha/resources

# Logs HA
journalctl -u pve-ha-lrm -f
journalctl -u pve-ha-crm -f
```

Common pitfalls:
- HA precisa de pelo menos 3 nós para funcionar bem (quorum)
- Storage shared (Ceph, NFS, iSCSI) é obrigatório para HA
- Sem watchdog ativo, fence não funciona

### 6. Performance degradada

```bash
# CPU
top
htop
pvesh get /nodes/<node>/status

# I/O
iotop -o
zpool iostat -v 5     # ZFS
ceph osd perf         # Ceph

# Memória
free -h
pvesh get /nodes/<node>/status | grep memory
```

KSM (kernel same-page merging) ajuda com VMs Linux similares:
```bash
systemctl status ksmtuned
cat /sys/kernel/mm/ksm/pages_shared
```

### 7. Web UI lenta ou inacessível

```bash
systemctl status pveproxy
systemctl restart pveproxy

# Logs
tail -f /var/log/pveproxy/access.log

# Verificar certificado expirado
pveproxy status
```

### 8. Disco cheio em /

```bash
df -h
du -sh /var/log/* | sort -h
du -sh /var/lib/vz/dump/*

# Logs comuns que crescem demais
journalctl --vacuum-size=500M

# Backups antigos
find /var/lib/vz/dump -name "*.vma*" -mtime +30 -ls
```

### 9. ZFS pool com erro

```bash
zpool status
zpool scrub <pool>   # iniciar scrub
zpool clear <pool>   # limpar erros temporários (cuidado)
zfs list -t snapshot
```

### 10. Ceph OSD down

```bash
ceph -s
ceph osd tree
ceph osd df

# Restart OSD específica
systemctl restart ceph-osd@<id>

# Ver logs
journalctl -u ceph-osd@<id> -n 100
```

## Checklist de saúde do cluster

```bash
# Rodar diariamente / via Zabbix
pvecm status | grep -q "Quorate: Yes" || echo "ALERTA: cluster sem quorum"
pvesm status | grep -q "inactive" && echo "ALERTA: storage inativo"
ha-manager status | grep -q "error" && echo "ALERTA: HA com erro"
df -h / | awk 'NR==2 { if ($5+0 > 80) print "ALERTA: disco / > 80%" }'
```
