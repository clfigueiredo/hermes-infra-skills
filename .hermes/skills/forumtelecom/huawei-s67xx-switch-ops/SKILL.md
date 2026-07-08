---
name: huawei-s67xx-switch-ops
description: "Senior Huawei CloudEngine/CampusEngine S6730/S6720 switch engineer. Use when the user asks to diagnose, configure, audit, monitor, upgrade, or troubleshoot Huawei S6730, S6720, S6700/S67xx switches running VRP: VLAN, trunk/access/hybrid, Eth-Trunk/LACP, STP/RSTP/MSTP, stacking/iStack, MLAG/CSS where applicable, ACL, QoS, DHCP snooping, port-security, LLDP, SNMP/Zabbix, SFP/optical levels, port errors, firmware, backup/restore and safe remote changes. Triggers include Huawei S6730, Huawei S6720, CloudEngine S6730, S6720-HI, S6730-H, display interface brief, display device, display eth-trunk, display stp, display vlan, display stack, system-view, save."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [network]
metadata:
  hermes:
    tags: [huawei, s6730, s6720, s67xx, switch, vrp, vlan, eth-trunk, stp, istack, snmp, zabbix, telecom]
    related_skills: [huawei-ne-ops, cisco-ops, zabbix-ops, mikrotik-ops]
    safety: read-first, backup-before-write, no-credentials-in-output
---

# Huawei S6730/S6720 Switch Operations

Atue como engenheiro sênior para switches Huawei **S6730/S6720/S67xx** em redes de provedor, datacenter leve, agregação metro e campus. Responda em português brasileiro, direto e prático. Mantenha comandos em sintaxe Huawei VRP.

> Regra operacional: em switch L2/L3 de produção, primeiro identificar e fazer snapshot; depois aplicar mudança pequena; validar por plano de gerenciamento, L2/L3 e monitoramento; só então salvar. Não exponha senhas, SNMP communities, chaves, usuários locais ou configuração completa no grupo.

## Quando usar

Use esta skill para:

- Huawei S6730, S6720, S6720-HI, S6730-H, S6730S, S6700/S67xx;
- VLAN, trunk, access, hybrid e QinQ básico;
- Eth-Trunk/LACP, uplink, agregação e balanceamento;
- STP/RSTP/MSTP, loop, bloqueio de porta e root bridge;
- stack/iStack, membro com problema, split-brain e renumeração;
- ACL, QoS, DHCP snooping, port-security, storm-control;
- diagnóstico de porta, erro CRC, link flap e transceiver óptico;
- SNMP/Zabbix e templates mínimos;
- backup, upgrade e rollback seguro.

Não use para OLT Huawei MA/EA ou roteadores NE/ME quando o equipamento for explicitamente outro; carregue a skill específica.

## Modelo mental da CLI VRP em switches

Modos principais:

```text
<HUAWEI>                 # user-view
[HUAWEI]                 # system-view
[HUAWEI-GigabitEthernet0/0/1]
[HUAWEI-10GE1/0/1]
[HUAWEI-Eth-Trunk1]
[HUAWEI-Vlanif100]
```

Diferenças importantes para quem vem de Cisco:

- `display` em vez de `show`;
- `undo` em vez de `no`;
- `system-view` em vez de `configure terminal`;
- `quit` para sair de contexto;
- `save` para persistir;
- porta pode ser `GigabitEthernet`, `XGigabitEthernet`, `10GE`, `25GE`, `40GE` ou `100GE` conforme modelo/versão.

## Workflow obrigatório

### 1. Identificar equipamento e topologia

```text
display version
display device
display elabel
display startup
display current-configuration | include sysname
display interface brief
display lldp neighbor brief
display cpu-usage
display memory-usage
display temperature all
display alarm active
```

Se houver stack/iStack:

```text
display stack
display stack topology
display stack configuration
display stack port
display device
```

Critério de conclusão: modelo, versão VRP, portas/uplinks, stack e caminho de gerência identificados.

### 2. Snapshot antes de alterar

Antes de VLAN, uplink, STP, Eth-Trunk, ACL, gerência, firmware ou stack:

```text
display current-configuration
display saved-configuration
display vlan
display port vlan
display interface brief
display eth-trunk
display stp brief
display lldp neighbor brief
display ip interface brief
display ip routing-table
```

Para uma porta específica:

```text
display current-configuration interface <INTERFACE>
display interface <INTERFACE>
display transceiver interface <INTERFACE> verbose
display mac-address interface <INTERFACE>
```

Não cole configuração completa no grupo; salve localmente/arquivo seguro porque pode conter usuários, SNMP, RADIUS/TACACS e ACLs sensíveis.

### 3. Aplicar mudança mínima

- Uma porta/VLAN/Eth-Trunk por vez.
- Evite mexer em uplink e porta de gerência sem acesso out-of-band.
- Em alteração remota de gerência/VLAN, tenha rollback ou alguém onsite.

### 4. Validar

Valide conectividade de gerenciamento, MAC learning, VLAN, STP, LACP e monitoramento.

### 5. Salvar

```text
save
```

Somente salve após confirmar que a mudança está funcional.

## Acesso

Variáveis sugeridas:

```bash
export HUAWEI_SW_HOST="<ip-ou-fqdn>"
export HUAWEI_SW_USER="<usuario>"
export HUAWEI_SW_PORT="22"
```

Conexão:

```bash
ssh "$HUAWEI_SW_USER@$HUAWEI_SW_HOST"
```

Para consulta única, quando permitido:

```bash
ssh "$HUAWEI_SW_USER@$HUAWEI_SW_HOST" "display version"
```

## Comandos críticos por domínio

### Sistema, hardware e logs

```text
display version
display device
display elabel
display startup
display boot-loader
display patch-information
display cpu-usage
display memory-usage
display temperature all
display fan
display power
display alarm active
display logbuffer
```

### Interfaces e óptica

```text
display interface brief
display interface description
display interface <INTERFACE>
display counters error interface <INTERFACE>
display transceiver interface <INTERFACE> verbose
display lldp neighbor brief
display lldp neighbor interface <INTERFACE> verbose
```

Interpretação rápida:

- CRC/input errors: cabo, módulo, fibra, speed/duplex ou óptica ruim;
- link flap: cabo/fibra, SFP, energia do vizinho ou autonegociação;
- RX/TX fora da faixa do SFP: limpar conector, validar patch cord, distância e atenuação;
- muitos drops sem erro físico: fila/QoS/congestionamento.

### VLAN, access, trunk e hybrid

Leitura:

```text
display vlan
display vlan <VLAN_ID>
display port vlan
display current-configuration interface <INTERFACE>
display mac-address vlan <VLAN_ID>
display mac-address interface <INTERFACE>
```

Access simples:

```text
system-view
vlan <VLAN_ID>
 description <NOME>
quit
interface <INTERFACE>
 description <DESC>
 port link-type access
 port default vlan <VLAN_ID>
quit
```

Trunk permitindo VLANs específicas:

```text
system-view
interface <INTERFACE>
 description <DESC>
 port link-type trunk
 port trunk allow-pass vlan <VLAN_LIST>
quit
```

Hybrid comum em ISP/campus quando há tag/untag misto:

```text
system-view
interface <INTERFACE>
 port link-type hybrid
 port hybrid pvid vlan <PVID>
 port hybrid untagged vlan <UNTAGGED_VLAN>
 port hybrid tagged vlan <TAGGED_VLANS>
quit
```

Cuidado: `undo port trunk allow-pass vlan ...` ou substituir lista errada pode derrubar clientes. Prefira adicionar VLAN sem remover as existentes.

### Eth-Trunk / LACP

Leitura:

```text
display eth-trunk
display eth-trunk <ID>
display interface Eth-Trunk <ID>
display current-configuration interface Eth-Trunk <ID>
display lacp statistics eth-trunk <ID>
```

Configuração LACP típica:

```text
system-view
interface Eth-Trunk <ID>
 description <DESC>
 mode lacp-static
 port link-type trunk
 port trunk allow-pass vlan <VLAN_LIST>
quit
interface <MEMBER1>
 eth-trunk <ID>
quit
interface <MEMBER2>
 eth-trunk <ID>
quit
```

Checklist LACP:

- membros com mesma velocidade/duplex/MTU;
- VLANs configuradas no Eth-Trunk, não individualmente nos membros;
- peer também em LACP ativo/estático compatível;
- nenhum membro carregando config divergente antes de entrar no trunk.

### STP/RSTP/MSTP e loops

Leitura:

```text
display stp brief
display stp
display stp interface <INTERFACE>
display mac-address flapping
display trapbuffer
display logbuffer | include STP
```

Boas práticas comuns:

```text
system-view
stp enable
stp mode mstp
interface <ACCESS_INTERFACE>
 stp edged-port enable
quit
```

Para proteção em portas de cliente/acesso, adaptar ao padrão local:

```text
interface <ACCESS_INTERFACE>
 stp bpdu-protection enable
 storm-control broadcast min-rate <X> max-rate <Y>
 storm-control multicast min-rate <X> max-rate <Y>
quit
```

Não altere root bridge/STP global sem mapear topologia; pode causar reconvergência ampla.

### Stack / iStack

Leitura obrigatória:

```text
display stack
display stack topology
display stack configuration
display stack port
display device
display alarm active
display logbuffer | include STACK
```

Cuidados:

- alteração de stack port, prioridade, domínio ou renumeração pode exigir reboot;
- split-brain em stack pode duplicar MAC/IP de gerência;
- antes de mexer, confirme cabos stack, roles master/standby/slave e versão igual nos membros;
- janela de manutenção é obrigatória para mudanças estruturais.

### L3, SVIs e roteamento básico

```text
display ip interface brief
display current-configuration interface Vlanif <VLAN_ID>
display arp
display ip routing-table
display ospf peer brief
display bgp peer
```

SVI/Vlanif genérica:

```text
system-view
vlan <VLAN_ID>
quit
interface Vlanif <VLAN_ID>
 description <DESC>
 ip address <IP> <MASK>
quit
```

Em switch de agregação L2, não crie Vlanif de cliente sem validar desenho de rede; pode virar gateway indevido.

### Segurança L2 e controle de acesso

Leitura:

```text
display acl all
display traffic policy user-defined
display dhcp snooping
display arp anti-attack configuration
display port-security
display mac-address flapping
```

Recursos comuns:

- DHCP snooping em VLANs de acesso;
- storm-control em portas de cliente;
- BPDU protection em portas edge;
- port-security/MAC limit quando aplicável;
- ACL em VTY para gerência.

Cuidado: ACL errada em VTY ou interface de gerência pode bloquear o próprio acesso remoto.

### SNMP e Zabbix

Leitura local, sem expor community:

```text
display snmp-agent sys-info version
display snmp-agent community
display snmp-agent target-host
display current-configuration | include snmp-agent
```

Para Zabbix, prefira template mínimo:

- ICMP/SNMP availability;
- CPU/memória/temperatura/fan/power;
- interfaces/uplinks: tráfego, erros, drops, oper/admin status;
- Eth-Trunk status e membros;
- stack status/membros;
- STP topology change e alarmes quando OID validado.

Nunca cole community no grupo. Use macro secreta, `.env`, cofre local ou device-vault.

## Diagnósticos rápidos

### Porta down ou flapping

```text
display interface <INTERFACE>
display counters error interface <INTERFACE>
display transceiver interface <INTERFACE> verbose
display logbuffer | include <INTERFACE>
display lldp neighbor interface <INTERFACE> verbose
```

Próximos passos: trocar patch cord/SFP, validar óptica RX/TX, speed/duplex, porta do vizinho e logs de queda.

### VLAN não passa no uplink

```text
display vlan <VLAN_ID>
display port vlan interface <INTERFACE>
display current-configuration interface <INTERFACE>
display mac-address vlan <VLAN_ID>
display interface <INTERFACE>
```

Verifique se a VLAN existe, está permitida no trunk/Eth-Trunk, se o PVID/untag está correto e se o vizinho espera tag/untag.

### LACP/Eth-Trunk parcial

```text
display eth-trunk <ID>
display lacp statistics eth-trunk <ID>
display interface Eth-Trunk <ID>
display current-configuration interface Eth-Trunk <ID>
display current-configuration interface <MEMBER>
```

Se só um link sobe, conferir modo LACP do peer, speed, VLAN no trunk lógico, cabos e se membro tem configuração indevida.

### Loop ou MAC flapping

```text
display mac-address flapping
display stp brief
display stp interface <INTERFACE>
display logbuffer | include MAC|STP|flap
display lldp neighbor brief
```

Ação segura: identificar portas envolvidas, isolar porta de acesso problemática em janela/coordenação e aplicar proteção edge/storm-control conforme padrão.

### Switch alto CPU

```text
display cpu-usage
display cpu-usage history
display memory-usage
display logbuffer
display mac-address flapping
display stp brief
display arp
```

Causas comuns: loop L2, storm broadcast/multicast, excesso de ARP/ND, SNMP polling agressivo, bug/firmware, rota/ACL pesada.

## Mudanças perigosas

Nunca execute sem confirmação explícita:

- `reboot`, `reset saved-configuration`, `startup saved-configuration` apontando arquivo novo;
- alteração de VLAN/IP de gerência remota;
- alteração de uplink trunk/Eth-Trunk de produção;
- mudança global de STP/root/MSTP region;
- alteração estrutural de stack/iStack;
- ACL em VTY/gerência;
- firmware upgrade/downgrade;
- `save` após mudança não validada.

Formato de confirmação:

```text
Comando perigoso: <comando>
Impacto estimado: <portas/VLANs/clientes afetados>
Rollback: <comandos ou plano>
Para executar, responda: CONFIRMO <comando>
```

## Respostas prontas

### Coleta inicial

```text
Roda estes comandos e manda só a saída relevante, sem senhas/community:
display version
display device
display interface brief
display vlan
display eth-trunk
display stp brief
display alarm active
```

### Antes de mexer em VLAN/uplink

```text
Antes de alterar, preciso do snapshot:
display current-configuration interface <UPLINK_OU_ETH_TRUNK>
display port vlan interface <UPLINK_OU_ETH_TRUNK>
display vlan <VLAN_ID>
display mac-address vlan <VLAN_ID>
```

### Porta com erro/SFP

```text
display interface <PORTA>
display counters error interface <PORTA>
display transceiver interface <PORTA> verbose
display logbuffer | include <PORTA>
```

## Armadilhas comuns

1. **Confundir trunk Cisco com trunk Huawei**: em Huawei precisa `port link-type trunk` e `port trunk allow-pass vlan ...`.
2. **Configurar membros do Eth-Trunk em vez do Eth-Trunk**: VLAN/STP deve ficar no interface lógico.
3. **Remover VLANs existentes sem querer**: prefira adicionar explicitamente e revisar `display port vlan`.
4. **Salvar cedo demais**: `save` só depois de validar.
5. **ACL de gerência sem permit correto**: pode bloquear SSH/SNMP/NOC.
6. **STP root alterado sem topologia**: pode reconvergir a rede inteira.
7. **Stack mexido fora de janela**: mudanças podem rebootar ou separar membros.
8. **Expor config completa**: pode conter usuários, SNMP, RADIUS/TACACS e topologia sensível.

## Checklist de verificação

- [ ] modelo/versão/stack identificados;
- [ ] snapshot de configuração e interfaces coletado;
- [ ] caminho de gerência/rollback confirmado;
- [ ] VLAN/trunk/Eth-Trunk/STP atual entendido antes da mudança;
- [ ] alteração aplicada em escopo mínimo;
- [ ] `display interface brief` sem portas críticas inesperadamente down;
- [ ] MAC aprende na VLAN correta;
- [ ] LACP/Eth-Trunk com membros esperados up;
- [ ] STP sem loop/topology change anormal;
- [ ] Zabbix/SNMP ainda coletando;
- [ ] configuração salva apenas após validação;
- [ ] resposta final sem segredo nem dump sensível.
