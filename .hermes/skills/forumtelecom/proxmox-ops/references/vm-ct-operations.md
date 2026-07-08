# Proxmox VM/CT — operações comuns

## Criar VM nova (KVM)

```bash
# 1. Criar VM básica
qm create 200 \
  --name my-vm \
  --memory 4096 \
  --cores 2 \
  --net0 virtio,bridge=vmbr0 \
  --bootdisk scsi0 \
  --scsihw virtio-scsi-pci

# 2. Criar disco (em local-lvm, 32G)
qm set 200 --scsi0 local-lvm:32

# 3. Adicionar ISO de boot
qm set 200 --ide2 local:iso/ubuntu-24.04.iso,media=cdrom

# 4. Configurar boot order
qm set 200 --boot order=ide2

# 5. Iniciar
qm start 200

# 6. Console
qm terminal 200          # serial
# ou via web UI noVNC
```

## Criar VM com cloud-init (mais rápido)

```bash
# Premissa: ter um template cloud-init pronto (ex: ID 9000)

qm clone 9000 200 --name my-vm --full
qm set 200 --memory 4096 --cores 2
qm set 200 --ipconfig0 ip=10.0.0.10/24,gw=10.0.0.1
qm set 200 --sshkeys ~/.ssh/id_ed25519.pub
qm set 200 --ciuser ubuntu --cipassword 'minha-senha'
qm resize 200 scsi0 +20G
qm start 200
```

## Criar container LXC

```bash
# 1. Baixar template
pveam update
pveam available --section system | grep ubuntu
pveam download local ubuntu-24.04-standard_24.04-1_amd64.tar.zst

# 2. Criar container
pct create 200 local:vztmpl/ubuntu-24.04-standard_24.04-1_amd64.tar.zst \
  --hostname my-ct \
  --memory 2048 \
  --swap 512 \
  --cores 2 \
  --rootfs local-lvm:8 \
  --net0 name=eth0,bridge=vmbr0,ip=10.0.0.20/24,gw=10.0.0.1 \
  --nameserver 8.8.8.8 \
  --password 'minha-senha' \
  --unprivileged 1 \
  --features nesting=1

# 3. Iniciar
pct start 200

# 4. Entrar
pct enter 200
```

## Migração entre nós

```bash
# VM live migration (online)
qm migrate 200 nó2 --online

# Com storage (se shared storage não existe)
qm migrate 200 nó2 --online --with-local-disks

# CT migration (precisa parar — LXC online migration tem limitações)
pct migrate 200 nó2 --restart

# Verificar status
qm status 200
pvesh get /cluster/tasks
```

## Snapshot e rollback

```bash
# Criar snapshot
qm snapshot 200 antes-update --description "Antes do update kernel"

# Listar
qm listsnapshot 200

# Rollback
qm rollback 200 antes-update

# Deletar snapshot
qm delsnapshot 200 antes-update
```

## Backup com vzdump

```bash
# Backup pontual
vzdump 200 --storage pbs --mode snapshot --compress zstd --notes-template "{{guestname}} manual"

# Backup com exclusão de discos
vzdump 200 --storage pbs --mode snapshot --exclude-path /tmp

# Backup todas VMs do nó
vzdump --all --storage pbs --mode snapshot

# Schedule (configurar via web UI ou /etc/pve/jobs.cfg)
```

## Restaurar backup

```bash
# Listar backups disponíveis
pvesm list pbs

# Restore VM (cria nova)
qmrestore pbs:backup/vm/200/2026-04-29T03:00:00Z 300 --storage local-lvm

# Restore CT
pct restore 300 pbs:backup/ct/200/2026-04-29T03:00:00Z --storage local-lvm
```

## Recursos comuns (CPU, RAM, disco)

```bash
# Aumentar RAM (online se hot-plug habilitado)
qm set 200 --memory 8192

# Aumentar CPU
qm set 200 --cores 4 --sockets 1

# Aumentar disco
qm resize 200 scsi0 +20G
# Depois, dentro da VM: growpart + resize2fs/xfs_growfs

# CT — basta resize, expand é automático
pct resize 200 rootfs +10G
```

## Console e troubleshooting

```bash
# Console serial
qm terminal 200

# Forçar shutdown se travou
qm stop 200

# Forçar destrava VM com lock
qm unlock 200

# Ver processos qemu
ps aux | grep "qm-200\|kvm"

# Logs específicos
journalctl -u qemu-server@200
journalctl -u pve-container@200
```

## Hot-plug

Para hot-plug funcionar, VM precisa ser configurada antes:
```bash
qm set 200 --hotplug network,disk,usb,memory,cpu
```

## Cloning para template

```bash
# 1. Configurar VM como você quer (instalar OS, agentes, configs base)
# 2. Limpar máquina (cloud-init, ssh keys, etc.)
# 3. Convert em template
qm template 200

# Agora 200 é template — usar para `qm clone`
```

## Comandos diagnósticos rápidos

```bash
# Top de CPU/RAM por VM
pvesh get /nodes/<node>/qemu --output-format json | jq '.[] | {vmid, name, cpu, mem}'

# Uso de disco por storage
pvesh get /nodes/<node>/storage

# VMs com mais I/O
iotop -o

# Latência disco
ioping -W /var/lib/vz/

# Verificar IOMMU (para PCIe passthrough)
dmesg | grep -e DMAR -e IOMMU
```
