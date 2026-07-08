---
name: mimosa-wireless-ops
description: "Use when the user asks to diagnose, configure, audit, align, monitor, or troubleshoot Mimosa wireless radios and antennas: C5c, C5x, C5, B5/B5c/B5-Lite, A5/A5c, point-to-point and point-to-multipoint ISP links, signal/SNR/MCS/noise/channel/GPS sync, bridge/VLAN, firmware, Mimosa Cloud, Web UI, SNMP and Zabbix checks."
version: 1.0.0
author: Hermes Tutor
license: MIT
platforms: [network]
metadata:
  hermes:
    tags: [mimosa, c5c, c5x, b5, a5, wireless, ptmp, ptp, isp, snmp, zabbix]
    related_skills: [ubiquiti-airmax-ops, mikrotik-ops, zabbix-ops]
---

# Mimosa Wireless Operations

Atue como engenheiro de rádio enlace ISP/MSP para equipamentos Mimosa, especialmente **C5c/C5x/C5** em cliente/PTMP e **B5/B5c/A5/A5c** em backhaul ou AP. Use a sequência **identificar → medir RF → validar bridge/VLAN → aplicar mudança pequena → testar tráfego**.

> Escopo principal: antenas Mimosa C5c e família C5 em clientes, com visão operacional também para APs A5/A5c e backhauls B5/B5c. A sintaxe e menus variam por firmware; confirme modelo e versão antes de orientar alteração.

## Postura operacional obrigatória

1. **Read-only primeiro**: coletar modelo, firmware, modo de operação, link status, RSSI, SNR, MCS/PHY rate, noise/interference, canal/largura, potência, uptime, VLAN/bridge e LAN antes de qualquer alteração.
2. **Não derrubar enlace remoto**: frequência, largura, potência, modo AP/Client, VLAN de gerência, IP de gerência, firmware e reset exigem confirmação quando podem cortar o acesso.
3. **Backup antes de alteração**: exportar configuração pela Web UI/Mimosa Cloud antes de mexer.
4. **Não expor segredos**: mascarar senha admin, PSK, SNMP community, chaves, IPs sensíveis e backups completos.
5. **Uma mudança por vez**: aplicar, aguardar reconexão, validar link/tráfego e só então seguir.

## Quando usar

- C5c com sinal ruim, throughput baixo ou desconexões;
- cliente C5/C5c/C5x não registra no AP A5/A5c;
- enlace PTP B5/B5c instável;
- ajuste de frequência, largura de canal, potência ou antena;
- bridge/VLAN sem tráfego;
- upgrade/downgrade de firmware;
- monitoramento por SNMP/Zabbix/Mimosa Cloud;
- auditoria de POP/setor PTMP.

## Identificação inicial

Pela Web UI ou Mimosa Cloud, colete:

```text
modelo exato
firmware
modo: Client/PTMP, AP, Backhaul/PTP
status do link/registro
SSID/AP conectado ou par remoto
frequência/canal/largura
potência TX/EIRP/regulatory domain
RSSI por chain
SNR
noise/interference/channel utilization
MCS/PHY rate TX/RX
throughput real
latência/perda
uptime
LAN speed/duplex
bridge/router/VLAN de gerência e serviço
GPS sync/sync source, quando aplicável
```

Se houver acesso por SSH/CLI, use apenas comandos read-only conhecidos do equipamento/firmware. Muitos ambientes Mimosa são operados principalmente por Web UI, Mimosa Cloud e SNMP; não invente comando CLI se a versão não expõe shell operacional.

## Backup seguro

Antes de alteração:

```text
Web UI / Mimosa Cloud → Configuration / Backup / Export
Salvar arquivo em local seguro
Verificar se o backup contém senha/PSK/SNMP antes de compartilhar
```

Nunca cole backup bruto no grupo. Se precisar mandar evidência, envie só trechos mascarados.

## Diagnóstico de RF para C5c/C5x/C5

Referência prática para enlace 5 GHz ISP:

```text
Sinal excelente: -45 a -60 dBm
Sinal bom:       -60 a -65 dBm
Atenção:         -66 a -72 dBm
Ruim:            pior que -72 dBm
SNR desejável:   > 25 dB
MCS/PHY estável: bom sinal + baixo ruído + Fresnel limpo
```

Checklist:

```text
1. RSSI das chains está equilibrado? Diferença > 5 dB indica alinhamento, cabo, conector, polarização ou antena.
2. SNR está baixo mesmo com RSSI forte? Suspeitar ruído/interferência ou potência excessiva.
3. MCS/PHY rate oscila? Ver interferência, largura de canal, distância, Fresnel e alinhamento.
4. Throughput baixo com rádio bom? Ver LAN 100M/1G, VLAN, switch, roteador, CPU e limite de plano.
5. Desconexão recorrente? Ver energia/PoE, cabo, conector, firmware, canal DFS, ruído e saturação do setor.
```

## Interferência, canal e largura

Para mudanças remotas:

- não trocar frequência/largura sem janela ou acesso alternativo;
- em PTMP, avaliar impacto em todos os clientes do setor;
- em PTP/backhaul, planejar os dois lados;
- se usa GPS/sync no AP/backhaul, validar sync antes de alterar canal/largura;
- preferir largura menor quando o ambiente RF está ruidoso e a meta é estabilidade.

Boas práticas:

```text
- potência máxima não é padrão; excesso de potência pode piorar SNR/ruído;
- alinhar fisicamente antes de compensar com potência;
- manter EIRP/regulatory domain correto;
- evitar canal DFS se houver quedas por radar/DFS e houver alternativa legal;
- documentar frequência/largura/setor antes de mexer.
```

## Bridge, VLAN e tráfego

Quando o link conecta mas não passa tráfego, validar:

```text
modo bridge vs router/NAT
VLAN de gerência
VLAN de serviço tagged/untagged
porta LAN negociando velocidade/duplex correto
switch/roteador permitindo a VLAN
MAC aprendido dos dois lados
MTU se houver PPPoE, QinQ, túnel ou transporte corporativo
loop/broadcast storm em bridge transparente
```

Testes objetivos:

```bash
ping <gateway-do-cliente>
ping <gateway-do-provedor>
traceroute <destino>
iperf3 -c <servidor>   # quando houver servidor controlado
```

Em switch/roteador de borda, conferir MAC/VLAN no equipamento conectado ao rádio.

## AP A5/A5c e setores PTMP

Para setor com muitos clientes:

```text
clientes conectados/desconectados
RSSI/SNR médio e piores clientes
MCS/PHY por cliente
airtime/utilização do setor
interferência/noise
GPS sync status, quando aplicável
capacidade do setor vs tráfego real
clientes com chain desequilibrada
```

Priorize corrigir os piores clientes e interferência antes de aumentar potência ou largura.

## Firmware

Sequência segura:

1. identificar modelo exato e firmware atual;
2. confirmar firmware correto para a família C5/C5x/C5c/B5/A5;
3. ler release notes quando possível;
4. fazer backup;
5. atualizar fora de horário crítico;
6. validar link, RSSI/SNR/MCS e tráfego depois;
7. não atualizar setor/AP e vários clientes ao mesmo tempo sem plano de rollback.

## SNMP, Mimosa Cloud e Zabbix

Use SNMP read-only e community forte. Não publicar community no grupo.

Validação básica por SNMP:

```bash
snmpwalk -v2c -c "$MIMOSA_SNMP_COMMUNITY" "$MIMOSA_HOST" sysDescr.0
snmpwalk -v2c -c "$MIMOSA_SNMP_COMMUNITY" "$MIMOSA_HOST" ifDescr
snmpwalk -v2c -c "$MIMOSA_SNMP_COMMUNITY" "$MIMOSA_HOST" ifOperStatus
```

Métricas mínimas úteis:

- disponibilidade/latência/perda;
- tráfego LAN/radio;
- RSSI/SNR por chain;
- MCS/PHY TX/RX;
- ruído/interferência/channel utilization;
- uptime e firmware;
- clientes conectados no AP;
- GPS/sync quando aplicável;
- LAN speed/duplex.

Para Zabbix, prefira template enxuto: disponibilidade, tráfego, RF principal e alertas de queda/baixo SNR, sem milhares de itens desnecessários.

## Comandos perigosos — exigir confirmação

Não executar sem confirmação explícita:

```text
reboot
factory reset / reset defaults
firmware upgrade/downgrade
restore config
alterar IP/VLAN de gerência
alterar modo AP/Client/Bridge/Router
alterar frequência/largura/potência em enlace remoto
alterar regulatory domain/country
```

## Relatório final padrão

```text
Status: OK/atenção/falha
Rádio: <modelo> / firmware <versão>
Modo: <C5c client / A5 AP / B5 PTP>
RF: RSSI <dBm>, SNR <dB>, MCS/PHY <rate>, ruído <dBm>, canal/largura <valor>
Rede: LAN <speed>, VLAN/bridge <resumo>
Ação: <verificado/alterado>
Validação: <ping/tráfego/cliente online>
Próximo passo: <se houver>
```

## Armadilhas comuns

1. **Tratar C5c como AP**: C5c normalmente aparece em cliente/PTMP; confirmar papel antes de orientar.
2. **Sinal forte e SNR ruim**: não resolver só com potência; investigar ruído/interferência.
3. **Chains desequilibradas**: pode ser antena desalinhada, cabo/conector, polarização ou obstrução de Fresnel.
4. **Mudar setor sem olhar clientes**: em PTMP, alteração no AP afeta todos os assinantes.
5. **Perder gerência por VLAN/IP**: confirmar rota/switch antes de aplicar.
6. **Firmware de família errada**: validar modelo exato antes do upload.
7. **Compartilhar backup cru**: pode conter credenciais e chaves.

## Checklist de validação

- [ ] modelo/firmware/papel identificados;
- [ ] backup feito antes de mudança;
- [ ] RSSI/SNR/MCS/noise/canal/largura coletados;
- [ ] bridge/VLAN/LAN validadas se o problema é tráfego;
- [ ] impacto em AP/setor/PTMP considerado;
- [ ] alteração aplicada uma por vez;
- [ ] ping/tráfego/cliente online validado depois;
- [ ] relatório final sem segredos.
