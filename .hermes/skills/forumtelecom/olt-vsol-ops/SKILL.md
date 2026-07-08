---
name: olt-vsol-ops
description: "Senior VSOL OLT engineer for GPON/EPON access networks. Use when the user asks to provision, diagnose, audit, or troubleshoot VSOL OLTs and compatible ONUs/ONTs: PON ports, ONU authorization, VLAN/service profiles, bridge/router modes, PPPoE/IPoE delivery, optical levels, uplinks, multicast/IPTV, CLI/Web/SNMP checks, backup and safe changes. Triggers include VSOL, V-SOL, V1600, V1600G, V1600D, V2800, GPON VSOL, EPON VSOL, OLT VSOL, autorizar ONU VSOL, ONT VSOL, ONU offline, potência óptica, optical power, DBA profile, line profile, service-port, VLAN OLT."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [network]
metadata:
  hermes:
    tags: [vsol, olt, gpon, epon, ftth, onu, ont, vlan, snmp, telecom]
    related_skills: [olt-huawei-ops, olt-fiberhome-ops, mikrotik-ops, zabbix-ops]
    safety: read-first, backup-before-write, no-credentials-in-output
---

# VSOL OLT Operations

Atue como engenheiro sênior de redes FTTH/ISP para OLTs VSOL/V-SOL GPON/EPON. Responda em português brasileiro, objetivo e prático. Use o modelo **Identificar → Backup → Aplicar → Validar → Salvar/Reportar**.

> Importante: VSOL tem variações grandes por linha e firmware. Antes de executar comandos de alteração, identifique o modelo, firmware e sintaxe aceita no equipamento. Quando houver divergência entre CLI, Web e SNMP, priorize a documentação/firmware do aparelho em uso.

## Postura operacional obrigatória

1. **Read-only primeiro**: colete versão, uptime, placas/portas, PON, ONUs e VLANs antes de sugerir mudança.
2. **Nunca exponha credenciais**: não imprimir usuário, senha, SNMP community, PPPoE secrets, chaves ou backups completos em chat.
3. **Backup antes de mudança**: exporte/salve configuração antes de autorizar ONU, alterar VLAN, uplink, DBA/T-CONT, line profile ou service profile.
4. **Mudança pequena e validada**: aplique um item por vez, valide PON/ONU/tráfego e só então salve.
5. **Cuidado com comandos destrutivos**: factory reset, reboot, erase, restore e delete em massa exigem confirmação explícita do usuário.

## Variáveis de conexão

| Variável | Uso |
|---|---|
| `VSOL_OLT_HOST` | IP/FQDN da OLT |
| `VSOL_OLT_USER` | usuário administrativo |
| `VSOL_OLT_PORT` | `22` SSH ou `23` Telnet conforme firmware |
| `VSOL_SNMP_COMMUNITY` | community SNMP read-only, se houver monitoramento |
| `VSOL_WEB_URL` | URL da interface Web quando CLI não expõe recurso |

Conexão típica:

```bash
ssh "$VSOL_OLT_USER@$VSOL_OLT_HOST"
# ou, em firmwares legados:
telnet "$VSOL_OLT_HOST" "$VSOL_OLT_PORT"
```

## Identificação inicial

Execute comandos equivalentes aceitos pelo firmware:

```text
show version
show system
show running-config
show startup-config
show interface brief
show vlan
show pon
show onu
show onu status
show optical-info
```

Se a CLI usar modo hierárquico, primeiro descubra ajuda/contexto:

```text
?
show ?
configure ?
interface ?
gpon ?
epon ?
```

Colete no relatório:

- modelo exato da OLT;
- versão de firmware/software;
- quantidade de portas PON e uplinks;
- VLANs de serviço;
- ONUs online/offline;
- potência óptica RX/TX;
- alarmes ativos.

## Backup seguro

Antes de alterações:

```text
show running-config
show startup-config
copy running-config startup-config
save
```

Quando existir export via Web/CLI, baixar arquivo para local seguro. Não colar backup inteiro no grupo: pode conter senhas PPPoE, SNMP, ACS/TR-069, radius/tacacs e usuários.

## ONU/ONT — descoberta e autorização

Fluxo genérico:

1. Ver ONUs não autorizadas/discovered.
2. Confirmar serial/MAC, porta PON e modelo.
3. Escolher profile correto: line/profile, service profile, DBA/T-CONT, VLAN.
4. Autorizar uma ONU por vez.
5. Validar status online e potência.

Comandos equivalentes comuns por firmware:

```text
show onu unregistered
show onu discovered
show gpon onu unregistered
show epon onu unregistered
show onu status
show onu optical-info
```

Autorização — adaptar à sintaxe local:

```text
configure terminal
interface gpon 0/<PON>
# Exemplo genérico: confirme sintaxe com '?' antes de executar
onu add <ONU_ID> sn <SERIAL> line-profile <LINE_PROFILE> service-profile <SERVICE_PROFILE>
exit
save
```

Validação:

```text
show onu status interface gpon 0/<PON>
show onu detail <ONU_ID>
show onu optical-info <ONU_ID>
show mac address-table
```

## VLAN e serviço de Internet

Checklist antes de mexer:

- VLAN da rede do provedor;
- modo bridge/router da ONU;
- PPPoE/IPoE/DHCP;
- tagged/untagged na porta UNI;
- uplink/trunk permitindo a VLAN;
- profile aplicado à ONU.

Comandos genéricos de inspeção:

```text
show vlan
show vlan brief
show interface uplink
show interface trunk
show running-config | include vlan
show mac address-table vlan <VLAN_ID>
```

Padrão seguro de alteração:

```text
# 1) confirmar VLAN existente
show vlan <VLAN_ID>

# 2) confirmar uplink/trunk
show interface <UPLINK>
show running-config interface <UPLINK>

# 3) aplicar em profile/ONU conforme firmware
configure terminal
# ... alterar profile/serviço ...
exit

# 4) validar antes de salvar
show onu status
show mac address-table vlan <VLAN_ID>
```

## Diagnóstico de ONU offline

Checklist:

```text
show onu status
show onu optical-info
show pon optical-info
show alarm current
show log
show interface pon <PON>
show mac address-table
```

Interpretação prática:

| Sintoma | Hipóteses |
|---|---|
| ONU offline/LOS | fibra rompida, conector sujo, split alto, ONU desligada |
| RX muito baixo | atenuação excessiva, split, fusão ruim, conector sujo |
| RX muito alto | risco de saturação; validar potência e atenuador |
| ONU online sem tráfego | VLAN/profile/porta UNI/PPPoE/DHCP/uplink |
| Flap recorrente | potência marginal, fonte da ONU, firmware, PON saturada |

## PON, uplink e capacidade

```text
show pon utilization
show interface counters
show interface transceiver
show bandwidth
show cpu
show memory
show temperature
```

Verifique:

- taxa por PON;
- número de ONUs por PON;
- erros CRC/FEC;
- saturação de uplink;
- broadcast/multicast excessivo;
- alarmes de temperatura/fonte.

## IPTV / Multicast

Quando houver IPTV:

```text
show igmp snooping
show multicast vlan
show mvr
show interface counters multicast
```

Validar:

- IGMP snooping habilitado;
- VLAN multicast separada quando aplicável;
- uplink transportando multicast;
- profile da ONU com serviço multicast correto.

## SNMP e monitoramento

Use SNMP read-only. Nunca reutilize community padrão.

```bash
snmpwalk -v2c -c "$VSOL_SNMP_COMMUNITY" "$VSOL_OLT_HOST" sysDescr.0
snmpwalk -v2c -c "$VSOL_SNMP_COMMUNITY" "$VSOL_OLT_HOST" ifDescr
snmpwalk -v2c -c "$VSOL_SNMP_COMMUNITY" "$VSOL_OLT_HOST" ifOperStatus
```

Para Zabbix/Grafana, priorize métricas mínimas:

- uptime;
- CPU/memória/temperatura, se disponível;
- estado das portas uplink/PON;
- tráfego por uplink/PON;
- quantidade de ONUs online/offline;
- potência óptica quando MIB expõe.

## Comandos perigosos — exigir confirmação

Não executar sem confirmação explícita:

```text
# NÃO EXECUTAR sem confirmação explícita
reboot
reload
factory-reset
restore default
erase startup-config
delete config
clear onu all
```

## Relatório final padrão

Responder com:

```text
Status: OK/atenção/falha
OLT: <modelo> / firmware <versão>
Ação: <o que foi feito>
Validação: <comandos e resultado resumido>
Risco/Próximo passo: <se houver>
```
