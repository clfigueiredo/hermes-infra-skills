---
name: eve-ng-ops
description: "Use when the user asks to install, operate, troubleshoot, back up, upgrade, or build network labs on EVE-NG/UNetLab: nested virtualization, Proxmox/VMware/bare metal deployment, web UI, labs, nodes, QEMU/IOL/Dynamips images, templates, fixpermissions, CPU/RAM/disk sizing, packet capture, bridges/cloud networks, performance, backups and safe handling of licensed vendor images."
version: 1.0.0
author: Hermes Tutor
license: MIT
metadata:
  hermes:
    tags: [eve-ng, unetlab, network-emulator, qemu, iol, dynamips, labs, virtualization, telecom]
    related_skills: [proxmox-ops, vmware-ops, docker-ops, cisco-ops, mikrotik-ops]
---

# EVE-NG Operations

Atue como engenheiro de laboratório de redes para EVE-NG/UNetLab. Ajude a instalar, dimensionar, operar, corrigir e criar laboratórios com imagens QEMU, IOL, Dynamips e equipamentos virtuais de fabricantes.

Referências públicas usadas como base: documentação oficial EVE-NG (`eve-ng.net`), práticas de instalação em Proxmox/VMware/bare metal e operação comum de labs ISP/MSP.

## Segurança e legalidade

1. **Não fornecer imagens proprietárias**: IOS, IOL, RouterOS CHR, FortiGate, Juniper, Huawei, etc. exigem licença/origem legítima. Oriente onde colocar e como validar, mas não compartilhe links piratas.
2. **Não expor credenciais**: não publicar usuários/senhas de imagens, labs, appliances ou backups.
3. **Backup antes de upgrade/fix em massa**: labs e imagens podem ser pesados e críticos.
4. **Mudanças destrutivas exigem confirmação**: apagar labs, imagens, banco, snapshots, limpar `/opt/unetlab` ou expandir disco.
5. **Validar nested virtualization**: sem VT-x/AMD-V exposto, labs QEMU ficam lentos ou não sobem.

## Quando usar

- instalar EVE-NG Community/Professional;
- subir EVE-NG em Proxmox, VMware ESXi/Workstation ou bare metal;
- corrigir node que não inicia;
- adicionar imagem QEMU/IOL/Dynamips;
- rodar `fixpermissions`;
- criar lab de MikroTik, Cisco, Huawei, FortiGate, OLT simulado etc.;
- configurar cloud/bridge para conectar lab na rede real;
- otimizar CPU/RAM/disco;
- backup/restore de labs e imagens;
- troubleshooting de console HTML5/Telnet/VNC/Wireshark.

## Arquitetura e caminhos importantes

```text
/opt/unetlab/labs/                 labs do usuário
/opt/unetlab/addons/qemu/          imagens QEMU/KVM
/opt/unetlab/addons/iol/bin/       imagens IOL
/opt/unetlab/addons/dynamips/      imagens Dynamips IOS
/opt/unetlab/html/                 web UI
/opt/unetlab/wrappers/             scripts/wrappers EVE
/opt/unetlab/tmp/                  runtime temporário de labs
```

Comando crítico após adicionar imagem/lab:

```bash
/opt/unetlab/wrappers/unl_wrapper -a fixpermissions
```

## Dimensionamento prático

Laboratório leve:

```text
4 vCPU
16 GB RAM
100-200 GB SSD
```

Laboratório ISP médio:

```text
8-16 vCPU
32-64 GB RAM
300+ GB SSD/NVMe
nested virtualization habilitada
```

Backbone pesado / múltiplos vendors:

```text
16+ vCPU
64-128+ GB RAM
NVMe
host dedicado ou Proxmox bem dimensionado
```

Regra: RAM e I/O acabam antes de CPU em labs com muitos appliances.

## Instalação recomendada

### Proxmox VE

Checklist da VM:

```text
CPU type: host
Nested virtualization: habilitada no host
BIOS: SeaBIOS ou OVMF conforme ISO
Disk: VirtIO/SCSI, SSD/NVMe preferencial
NIC: VirtIO
RAM: reservar conforme labs
```

Validações no host Proxmox:

```bash
# Intel
cat /sys/module/kvm_intel/parameters/nested 2>/dev/null
# AMD
cat /sys/module/kvm_amd/parameters/nested 2>/dev/null

egrep -o 'vmx|svm' /proc/cpuinfo | head
```

Se nested não estiver ativo, ajustar no Proxmox com cautela e reboot do host se necessário.

### VMware / ESXi

- habilitar “Expose hardware assisted virtualization to the guest OS”;
- usar adaptador VMXNET3 quando possível;
- datastore em SSD;
- evitar oversubscription excessiva.

### Bare metal

- instalar pela ISO oficial EVE-NG;
- IP fixo;
- DNS/NTP corretos;
- disco suficiente;
- acesso SSH restrito.

## Pós-instalação e health check

```bash
hostname -I
uptime
free -h
df -h
lsblk
lscpu | egrep 'Model name|CPU\(s\)|Virtualization'

systemctl status apache2 --no-pager
systemctl status mysql --no-pager 2>/dev/null || systemctl status mariadb --no-pager

ss -lntp | egrep ':80|:443|:22|:32768|:32769|:3389|:5900'
```

No browser:

```text
http://<ip-do-eve>/
Login inicial conforme instalação/documentação oficial.
```

Critério: UI abre, login funciona, lab simples abre e node inicia.

## Adicionar imagens QEMU

Fluxo genérico:

```bash
mkdir -p /opt/unetlab/addons/qemu/<template-versao>
# copiar imagem licenciada para o diretório correto
cd /opt/unetlab/addons/qemu/<template-versao>
# nomes comuns: virtioa.qcow2, hda.qcow2, hdb.qcow2 — depende do template
qemu-img info *.qcow2
/opt/unetlab/wrappers/unl_wrapper -a fixpermissions
```

Boas práticas:

- seguir nome de pasta esperado pelo template EVE;
- validar `qemu-img info` antes de iniciar;
- não renomear aleatoriamente se a template espera `virtioa.qcow2`;
- manter inventário de versão/licença;
- testar 1 node antes de montar lab grande.

## Adicionar IOL

```bash
mkdir -p /opt/unetlab/addons/iol/bin
# copiar binários IOL licenciados para o diretório
/opt/unetlab/wrappers/unl_wrapper -a fixpermissions
```

Observações:

- IOL depende de licença/origem legítima;
- problemas de permissão são comuns;
- se node não inicia, olhar logs e permissões antes de culpar imagem.

## Adicionar Dynamips IOS

```bash
mkdir -p /opt/unetlab/addons/dynamips
# copiar imagem licenciada
/opt/unetlab/wrappers/unl_wrapper -a fixpermissions
```

Dynamips é útil para IOS clássico, mas escala pior que appliances modernos. Para labs grandes, preferir imagens QEMU otimizadas quando disponíveis.

## Criar e operar labs

Checklist de lab bom:

```text
Nome claro
Objetivo do lab
Topologia simples primeiro
IPs documentados
Usuário/senha de lab em cofre/local, não no grupo
Cloud/bridge só quando necessário
Snapshots/exports antes de mudanças grandes
```

Ordem segura:

1. criar lab vazio;
2. adicionar poucos nodes;
3. ligar e validar console;
4. conectar links;
5. configurar endereçamento;
6. salvar configs nos equipamentos;
7. exportar/backup quando pronto.

## Conectar lab à rede real

EVE usa networks/clouds para bridge com interfaces do host. Antes de conectar:

```bash
ip link
ip addr
bridge link 2>/dev/null
brctl show 2>/dev/null
```

Cuidados:

- risco de loop L2;
- DHCP indesejado vazando para rede real;
- broadcast storm;
- VLAN trunk mal configurado;
- lab anunciando rotas em produção;
- firewall/NAT do host.

Para labs de alunos, preferir NAT/isolado. Conectar em produção só com confirmação e plano.

## Troubleshooting: node não inicia

Checklist:

```bash
free -h
df -h
lscpu | egrep 'Virtualization|CPU\(s\)'
ls -lah /opt/unetlab/addons/qemu/<imagem>/
qemu-img info /opt/unetlab/addons/qemu/<imagem>/*.qcow2
/opt/unetlab/wrappers/unl_wrapper -a fixpermissions

tail -100 /var/log/syslog 2>/dev/null
dmesg | tail -80
```

Causas comuns:

```text
nested virtualization ausente
imagem com nome errado
pasta de template errada
permissão incorreta
RAM insuficiente
disco cheio
imagem corrompida
CPU incompatível
template EVE não corresponde ao appliance
```

## Troubleshooting: console não abre

Verificar:

```text
tipo de console: telnet / VNC / RDP / HTML5
popup bloqueado no navegador
porta bloqueada no firewall
node realmente está ligado
serviços web do EVE ativos
```

Comandos:

```bash
ss -lntp | egrep ':327|:590|:3389|:80|:443'
systemctl restart apache2
```

Evite reiniciar serviços durante lab ativo sem avisar usuários.

## Performance e estabilidade

Otimizações comuns:

```text
CPU type host na VM EVE
nested virtualization habilitada
SSD/NVMe
não superalocar RAM demais
usar imagens qcow2 enxutas
parar nodes/labs não usados
monitorar load average e iowait
```

Comandos:

```bash
uptime
free -h
df -h
iostat -xz 1 5 2>/dev/null || true
ps aux --sort=-%mem | head
ps aux --sort=-%cpu | head
```

## Backup e restore

Backup mínimo:

```bash
mkdir -p /backup/eve-ng
rsync -aH --numeric-ids /opt/unetlab/labs/ /backup/eve-ng/labs/
rsync -aH --numeric-ids /opt/unetlab/addons/ /backup/eve-ng/addons/
```

Backup compactado de labs:

```bash
tar czf /backup/eve-ng-labs-$(date +%F).tar.gz /opt/unetlab/labs
```

Antes de backup grande, conferir espaço:

```bash
du -sh /opt/unetlab/labs /opt/unetlab/addons
df -h /backup /opt/unetlab 2>/dev/null
```

Restore:

```bash
rsync -aH --numeric-ids /backup/eve-ng/labs/ /opt/unetlab/labs/
rsync -aH --numeric-ids /backup/eve-ng/addons/ /opt/unetlab/addons/
/opt/unetlab/wrappers/unl_wrapper -a fixpermissions
```

## Upgrade

Antes de atualizar:

```bash
cat /etc/issue
apt update
apt list --upgradable 2>/dev/null | head
rsync -aH --numeric-ids /opt/unetlab/labs/ /backup/eve-ng/labs-pre-upgrade/
rsync -aH --numeric-ids /opt/unetlab/addons/ /backup/eve-ng/addons-pre-upgrade/
```

Só atualizar com janela, backup e caminho de rollback. EVE-NG Community/Professional podem ter diferenças de repositório/licença.

## Monitoramento Zabbix

Itens mínimos:

```text
ping/agent do host
CPU/load/iowait
RAM/swap
disco / e /opt/unetlab
serviço apache2
serviço mysql/mariadb
porta 80/443
quantidade de qemu/kvm ativos
backup recente
```

Comandos para descoberta simples:

```bash
pgrep -af 'qemu|dynamips|iol' | wc -l
du -sh /opt/unetlab/labs /opt/unetlab/addons
```

## Comandos perigosos — exigir confirmação

Não executar sem confirmação explícita:

```text
rm -rf /opt/unetlab/*
apagar /opt/unetlab/addons
apagar /opt/unetlab/labs
upgrade de sistema/EVE
restore sobrescrevendo produção
reiniciar host EVE durante lab ativo
conectar bridge/cloud à rede real
limpar /opt/unetlab/tmp em produção ativa
```

## Relatório final padrão

```text
Status: OK/atenção/falha
EVE-NG: <versão/host>
Ação: <instalação/lab/imagem/troubleshooting>
Validação: <UI abriu/node iniciou/console OK/performance>
Risco: <se houver>
Próximo passo: <objetivo>
```

## Armadilhas comuns

1. **Sem nested virtualization**: QEMU até aparece, mas fica lento ou falha.
2. **Imagem na pasta errada**: EVE depende do nome de diretório/template.
3. **Não rodar fixpermissions**: causa clássica de node que não inicia.
4. **Disco cheio em `/opt/unetlab`**: labs param de salvar/iniciar.
5. **Conectar lab na rede real sem controle**: pode gerar loop, DHCP indevido ou rota errada.
6. **Usar imagem sem licença**: risco legal; não compartilhar artefatos proprietários.
7. **Superalocar VM**: muitos nodes com pouca RAM derrubam estabilidade.
8. **Upgrade sem backup**: pode perder labs/templates customizados.

## Checklist de validação

- [ ] EVE-NG identificado e acessível;
- [ ] CPU/RAM/disco/nested virtualization validados;
- [ ] serviços web/banco OK;
- [ ] labs e imagens com backup antes de mudança;
- [ ] imagem adicionada no diretório correto;
- [ ] `fixpermissions` executado quando necessário;
- [ ] node de teste iniciou e console abriu;
- [ ] rede/cloud validada sem risco de loop;
- [ ] relatório final sem credenciais nem imagens proprietárias.
