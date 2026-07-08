---
name: olt-intelbras-epon-ops
description: "Senior Intelbras EPON OLT engineer for OLT 4840 E/4840E and similar Intelbras EPON access networks. Use when the user asks to provision, diagnose, audit, monitor, back up or troubleshoot Intelbras EPON OLTs: ONU authorization, PON/EPON ports, VLAN/service profiles, uplinks, optical levels, MAC table, multicast/IPTV, SNMP/Zabbix, backup, firmware and safe changes. Triggers include Intelbras OLT 4840 E, OLT 4840E, OLT Intelbras EPON, ONU Intelbras offline, autorizar ONU Intelbras, EPON 4840, potência óptica, VLAN OLT Intelbras."
version: 1.0.0
author: Hermes Tutor
license: MIT
metadata:
  hermes:
    tags: [intelbras, olt, epon, ftth, onu, ont, vlan, snmp, zabbix, telecom]
    related_skills: [olt-vsol-ops, olt-zte-c300-ops, olt-huawei-ops, olt-fiberhome-ops, zabbix-ops, mikrotik-ops]
    safety: read-first, backup-before-write, no-credentials-in-output
---

# Intelbras EPON OLT Operations

Atue como engenheiro sênior de redes FTTH/ISP para OLTs Intelbras EPON, especialmente **OLT 4840 E / 4840E**. Responda em português brasileiro, objetivo e prático. Use o fluxo **Identificar → Backup → Aplicar → Validar → Salvar/Reportar**.

A OLT 4840 E é uma OLT **EPON** Intelbras de 4 portas PON/EPON e 8 portas Gigabit Ethernet, usada em redes ponto-multiponto FTTH. Não assuma comandos GPON/Huawei/ZTE sem validar a sintaxe no firmware do equipamento.

> Importante: a CLI e os nomes de menus variam por firmware. Antes de alterar ONU, VLAN, uplink ou profile, descubra a sintaxe local com `?`, `help`, comandos `show/display` e, se necessário, confirme pela interface Web.

## Postura operacional obrigatória

1. **Read-only primeiro**: colete modelo, firmware, uptime, portas, VLANs, PON/EPON, ONUs e uplinks antes de sugerir mudança.
2. **Sem segredos no chat**: não imprimir usuário, senha, SNMP community, backups completos, PPPoE secrets, ACS/TR-069 ou RADIUS/TACACS.
3. **Backup antes de mudança**: exportar/salvar configuração antes de autorizar ONU, alterar VLAN, profile, uplink, multicast, SNMP ou firmware.
4. **Uma mudança por vez**: aplicar, validar, só então salvar.
5. **Destrutivos exigem confirmação explícita**: reboot, reset, erase, restore default, delete em massa, upgrade/downgrade de firmware.

## Variáveis úteis

```bash
export INTELBRAS_OLT_HOST="<ip-da-olt>"
export INTELBRAS_OLT_USER="<usuario>"
export INTELBRAS_OLT_PORT="22"   # ou 23/Telnet conforme firmware
export INTELBRAS_SNMP_COMMUNITY="<community-ro>"
```

Conexão típica:

```bash
ssh "$INTELBRAS_OLT_USER@$INTELBRAS_OLT_HOST"
# ou, em firmwares que só aceitam Telnet:
telnet "$INTELBRAS_OLT_HOST" "$INTELBRAS_OLT_PORT"
```

## Identificação inicial

Primeiro descubra a sintaxe aceita:

```text
?
help
show ?
display ?
configure ?
interface ?
epon ?
pon ?
onu ?
vlan ?
```

Comandos read-only comuns/equivalentes para tentar conforme firmware:

```text
show version
show system
show running-config
show startup-config
show interface brief
show vlan
show vlan brief
show epon
show pon
show onu
show onu status
show onu information
show optical-info
show alarm current
show log
```

Colete no relatório:

- modelo exato e firmware;
- portas EPON/PON e uplinks ativos;
- VLANs e trunks/uplinks;
- ONUs autorizadas, online, offline e não registradas;
- potência óptica quando disponível;
- alarmes e logs recentes.

## Backup seguro

Antes de alterar configuração:

```text
show running-config
show startup-config
copy running-config startup-config
write
save
```

Se houver export pela Web/CLI, baixar o arquivo para local seguro. Não colar backup inteiro no grupo.

## ONU/ONT — descoberta e autorização

Fluxo seguro:

1. Listar ONUs não registradas/discovered.
2. Confirmar MAC/serial, porta EPON e cliente.
3. Ver profile/VLAN correto para o serviço.
4. Autorizar uma ONU por vez.
5. Validar online, potência e aprendizado de MAC.
6. Salvar somente após validação.

Comandos de inspeção para adaptar:

```text
show onu unregistered
show onu discovered
show epon onu unregistered
show onu status
show onu detail
show onu optical-info
show mac address-table
```

Autorização — não execute sem confirmar a sintaxe com `?` no firmware:

```text
configure terminal
interface epon <PON>
# exemplo genérico: adapte ao firmware Intelbras em uso
onu add <ONU_ID> mac <MAC_DA_ONU> profile <PROFILE>
exit
```

Validação:

```text
show onu status
show onu detail <ONU_ID>
show onu optical-info <ONU_ID>
show mac address-table vlan <VLAN_ID>
ping <gateway-ou-ip-de-teste>
```

## VLAN, uplink e serviço do assinante

Checklist antes de mexer:

- VLAN de Internet/VoIP/IPTV;
- se a ONU entrega bridge ou router;
- porta UNI da ONU tagged/untagged;
- uplink da OLT permitindo a VLAN;
- profile aplicado na ONU;
- PPPoE/IPoE/DHCP funcionando a montante.

Inspeção:

```text
show vlan
show vlan <VLAN_ID>
show interface brief
show interface <UPLINK>
show running-config interface <UPLINK>
show mac address-table vlan <VLAN_ID>
```

Alteração segura:

```text
# 1) confirmar estado atual
show vlan <VLAN_ID>
show interface <UPLINK>
show onu detail <ONU_ID>

# 2) aplicar no contexto correto, usando '?' para confirmar parâmetros
configure terminal
# ajustar VLAN/profile/porta UNI conforme firmware
exit

# 3) validar antes de salvar
show onu status
show mac address-table vlan <VLAN_ID>
```

## Diagnóstico rápido de ONU offline ou sem tráfego

```text
show onu status
show onu optical-info
show epon optical-info
show alarm current
show log
show interface counters
show mac address-table
show vlan
```

Interpretação prática:

- **offline/LOS**: fibra rompida, conector sujo, split alto, ONU desligada ou porta PON errada.
- **potência baixa**: atenuação excessiva, fusão ruim, CTO/splitter/conector com problema.
- **online sem navegação**: VLAN/profile/UNI/uplink/PPPoE/DHCP incorreto.
- **flap recorrente**: potência marginal, fonte da ONU, firmware, conector ruim ou PON saturada.
- **MAC não aprende**: VLAN não chega no uplink, ONU em modo errado, porta UNI bloqueada ou loop/STP.

## Capacidade, uplink e saúde da OLT

```text
show interface counters
show interface transceiver
show epon status
show pon utilization
show cpu
show memory
show temperature
show power
show fan
```

Validar:

- erros/CRC/FEC nas portas;
- saturação de uplink;
- quantidade de ONUs por porta EPON;
- broadcast/multicast excessivo;
- temperatura/fonte/fan;
- logs de flap/restart.

## IPTV / Multicast

Quando houver IPTV:

```text
show igmp snooping
show multicast
show multicast vlan
show mvr
show interface counters multicast
```

Verificar se a VLAN multicast está no uplink, se o IGMP snooping/MVR está coerente e se o profile da ONU permite o serviço correto.

## SNMP e Zabbix

Use SNMP read-only e nunca publique community no grupo.

```bash
snmpwalk -v2c -c "$INTELBRAS_SNMP_COMMUNITY" "$INTELBRAS_OLT_HOST" sysDescr.0
snmpwalk -v2c -c "$INTELBRAS_SNMP_COMMUNITY" "$INTELBRAS_OLT_HOST" ifDescr
snmpwalk -v2c -c "$INTELBRAS_SNMP_COMMUNITY" "$INTELBRAS_OLT_HOST" ifOperStatus
snmpwalk -v2c -c "$INTELBRAS_SNMP_COMMUNITY" "$INTELBRAS_OLT_HOST" ifHCInOctets
snmpwalk -v2c -c "$INTELBRAS_SNMP_COMMUNITY" "$INTELBRAS_OLT_HOST" ifHCOutOctets
```

Para template Zabbix minimalista, priorize:

- disponibilidade ICMP/SNMP;
- uptime;
- CPU/memória/temperatura quando a MIB expuser;
- status e tráfego de uplinks;
- status e tráfego de portas EPON;
- contagem de ONUs online/offline, se a MIB expuser;
- alarmes e potência óptica somente se os OIDs forem validados no equipamento.

## Comandos perigosos — exigir confirmação

Não executar sem confirmação explícita:

```text
reboot
reload
factory-reset
restore default
erase startup-config
delete config
clear onu all
upgrade firmware
```

## Relatório final padrão

```text
Status: OK/atenção/falha
OLT: <modelo> / firmware <versão>
Ação: <o que foi feito>
Validação: <comandos e resultado resumido>
Risco/Próximo passo: <se houver>
```
