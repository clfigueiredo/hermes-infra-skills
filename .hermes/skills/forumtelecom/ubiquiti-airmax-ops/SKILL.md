---
name: ubiquiti-airmax-ops
description: "Use when the user asks to diagnose, configure, audit, align, monitor, or troubleshoot Ubiquiti airMAX radios and antennas: airMAX AC, airOS M/M5, NanoStation, NanoBeam, LiteBeam, PowerBeam, Rocket, Bullet, point-to-point and point-to-multipoint wireless links, signal/CCQ/noise/channel/frequency, bridge mode, VLAN, firmware, SSH/Web/UISP/SNMP checks."
version: 1.0.0
author: Hermes Tutor
license: MIT
platforms: [network]
metadata:
  hermes:
    tags: [ubiquiti, airmax, airos, m5, ac, wireless, ptp, ptmp, isp, snmp]
    related_skills: [mikrotik-ops, zabbix-ops]
---

# Ubiquiti airMAX Operations

Atue como engenheiro de rádio enlace ISP/MSP para Ubiquiti airMAX AC e airOS M/M5. Use abordagem **identificar → medir rádio → validar bridge/VLAN → aplicar mudança pequena → testar tráfego**.

> Escopo: NanoStation M5/AC, NanoBeam M5/AC, LiteBeam, PowerBeam, Rocket M/AC, Bullet e famílias airMAX similares. Para UniFi Wi-Fi corporativo ou airFiber dedicado, confirme a linha antes de aplicar comandos.

## Postura operacional obrigatória

1. **Read-only primeiro**: colete modelo, firmware, modo wireless, sinal, CCQ/airMAX quality/capacity, ruído, canal, largura, distância, LAN/VLAN e uptime antes de sugerir mudança.
2. **Não derrubar enlace sem confirmação**: trocar frequência, largura de canal, potência, country code, modo AP/Station, bridge/router, VLAN de gerência ou firmware pode derrubar acesso remoto.
3. **Backup antes de alteração**: exporte configuração pela Web/UISP ou salve `/tmp/system.cfg` via SSH antes de mexer.
4. **Não expor segredos**: ocultar senhas, WPA keys, SNMP community, PPPoE, IPs públicos sensíveis e backups completos.
5. **Alteração uma por vez**: mudar um parâmetro, aguardar reconexão, validar sinal/tráfego e só então seguir.

## Quando usar

- enlace PTP/PTMP instável;
- sinal ruim ou CCQ baixo;
- cliente desconectando em Rocket/AP;
- ajuste de frequência/canal/largura/potência;
- VLAN/bridge sem passar tráfego;
- upgrade/downgrade de firmware airOS;
- monitoramento SNMP/Zabbix/UISP;
- auditoria de configuração de antenas AC ou M5.

## Identificação inicial

Via Web/UISP, colete:

```text
modelo
versão airOS/firmware
modo wireless: AP / Station / PtP / PtMP
SSID/enlace
frequência/canal/largura
potência TX/EIRP/country
signal/RSSI por chain
noise floor
SNR
CCQ / airMAX Quality / airMAX Capacity
TX/RX rate
LAN speed/duplex
uptime
```

Via SSH, comandos read-only comuns variam por firmware, mas estes costumam ajudar:

```bash
ssh "$UBNT_USER@$UBNT_HOST"

# identificação
cat /etc/version 2>/dev/null
cat /proc/ubnthal/system.info 2>/dev/null
cat /tmp/system.cfg 2>/dev/null | egrep '^(wireless|netconf|bridge|vlan|snmp|system)'

# estado de rádio/rede
ifconfig
brctl show 2>/dev/null
route -n
cat /proc/net/wireless 2>/dev/null
iwconfig 2>/dev/null
wstalist 2>/dev/null
mca-status 2>/dev/null
```

Se o comando não existir, use `?`, `help`, `ls /sbin /usr/bin` e valide pela interface Web. Não force sintaxe de outro firmware.

## Backup seguro

Antes de alterar:

```bash
ssh "$UBNT_USER@$UBNT_HOST" 'cat /tmp/system.cfg' > "backup-${UBNT_HOST}-$(date +%F-%H%M).cfg"
```

Depois, confira se o arquivo não contém senha/chave antes de compartilhar:

```bash
grep -Ei 'pass|password|key|secret|community|pppoe' backup-*.cfg
```

Não cole o backup bruto no grupo.

## Diagnóstico rápido de enlace

### Sinal e qualidade

Referência prática para 5 GHz ISP:

```text
Sinal excelente: -45 a -60 dBm
Sinal bom:       -60 a -65 dBm
Atenção:         -66 a -72 dBm
Ruim:            pior que -72 dBm
SNR desejável:   > 25 dB
CCQ/Quality:     > 85% bom; < 70% investigar
```

Checklist:

```text
1. Os dois lados enxergam sinal parecido?
2. Chains estão equilibradas? Diferença > 5 dB indica alinhamento/cabo/conector/polarização.
3. Noise floor piorou? Procurar interferência.
4. CCQ baixo com sinal bom? Suspeitar interferência, excesso de cliente, largura alta, firmware ou airMAX mal ajustado.
5. TX/RX rate oscila? Ver canal, largura, DFS, potência excessiva e Fresnel.
```

### Interferência e canal

Use AirView/Site Survey pela Web quando disponível. Em mudança remota:

- evite trocar canal sem acesso alternativo;
- prefira janela de manutenção;
- em PTP, ajuste os dois lados com plano de rollback;
- para PTMP, avalie todos os clientes antes de reduzir/aumentar largura.

Boas práticas:

```text
- largura menor melhora robustez em ambiente ruidoso;
- potência máxima nem sempre melhora: pode saturar e aumentar ruído;
- manter EIRP dentro da regulamentação/localidade;
- evitar canal DFS se o enlace sofre quedas por radar/DFS, quando permitido.
```

## Bridge, VLAN e LAN

Checklist para enlace que conecta mas não passa tráfego:

```bash
brctl show 2>/dev/null
ifconfig
cat /tmp/system.cfg 2>/dev/null | egrep 'bridge|vlan|mgmt|netconf|eth|ath'
```

Validar:

- modo bridge vs router;
- VLAN de gerência;
- VLANs tagged/untagged no switch/roteador;
- MTU quando passa PPPoE/MPLS/túneis;
- LAN negociando 100M/1G full duplex;
- loop/broadcast storm em bridge transparente;
- MAC table do switch nas duas pontas.

## Alterações seguras

Antes de aplicar:

```text
Plano: <alteração>
Risco: <pode derrubar por X minutos>
Rollback: <voltar frequência/largura/potência/config anterior>
Janela: <horário>
```

Em airOS, mudanças feitas por Web geralmente exigem **Change → Apply**. Via CLI, persistência pode variar por firmware; só use `cfgmtd`, `save` ou scripts de commit se tiver certeza do modelo/versão. Preferir Web/UISP para mudanças persistentes quando disponível.

## Upgrade de firmware

Sequência segura:

1. identificar modelo exato e firmware atual;
2. baixar firmware correto da linha M ou AC, sem misturar plataformas;
3. confirmar espaço/energia/acesso local ou rollback;
4. fazer backup;
5. atualizar um rádio por vez;
6. validar enlace e tráfego antes do próximo.

Nunca atualizar AP remoto crítico sem janela e plano de acesso local.

## Monitoramento SNMP/Zabbix

Ativar somente SNMP read-only e community forte. Não publicar community no grupo.

Comandos de validação:

```bash
snmpwalk -v2c -c "$UBNT_SNMP_COMMUNITY" "$UBNT_HOST" sysDescr.0
snmpwalk -v2c -c "$UBNT_SNMP_COMMUNITY" "$UBNT_HOST" ifDescr
snmpwalk -v2c -c "$UBNT_SNMP_COMMUNITY" "$UBNT_HOST" ifOperStatus
```

Métricas mínimas úteis:

- disponibilidade/latência;
- tráfego LAN/WLAN;
- sinal RSSI/SNR;
- CCQ/airMAX quality/capacity;
- ruído;
- TX/RX rate;
- clientes conectados no AP;
- uptime e firmware.

## Comandos perigosos — exigir confirmação

Não executar sem confirmação explícita:

```text
reboot
reset to defaults
factory reset
firmware upgrade/downgrade
change frequency/channel width/power on remote-only link
change management VLAN/IP
change wireless mode AP/Station
restore config
```

## Relatório final padrão

```text
Status: OK/atenção/falha
Rádio: <modelo> / firmware <versão>
Enlace: <AP/Station/PTP/PTMP>
Medições: sinal <dBm>, SNR <dB>, CCQ/Quality <%%>, ruído <dBm>, TX/RX <rate>
Ação: <o que foi verificado/alterado>
Validação: <ping/tráfego/uptime/cliente online>
Próximo passo: <se houver>
```

## Armadilhas comuns

1. **Misturar airMAX AC com linha M/M5**: comandos e firmware podem diferir.
2. **Ajustar só um lado do PTP**: frequência/largura/SSID/segurança precisam casar.
3. **Sinal forte demais**: pode saturar rádio; não usar potência máxima como padrão.
4. **CCQ baixo com sinal bom**: normalmente é interferência, largura excessiva ou ambiente RF ruim.
5. **Perder gerência por VLAN/IP**: confirmar rota e switch antes de aplicar.
6. **Firmware errado**: validar modelo exato antes do upload.
7. **Compartilhar config bruta**: pode conter senha Wi-Fi, SNMP e acesso administrativo.

## Checklist de validação

- [ ] modelo/firmware identificados;
- [ ] backup feito antes de alteração;
- [ ] sinal, SNR, ruído, CCQ/quality e rates coletados;
- [ ] bridge/VLAN/LAN validadas quando o problema é tráfego;
- [ ] mudança aplicada uma por vez;
- [ ] ping/tráfego/cliente online validado depois;
- [ ] relatório final sem segredos.
