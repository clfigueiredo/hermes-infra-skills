---
name: olt-zte-c300-ops
description: "Senior ZTE ZXA10 C300/C320 OLT engineer for GPON/EPON access networks. Use when the user asks to provision, diagnose, audit, or troubleshoot ZTE OLTs and ONUs/ONTs: C300, C320, ZXA10, GTGO, GTGH, ONU authorization, GPON ONU, VLAN/service-port, T-CONT/GEM, PPPoE/IPoE delivery, optical levels, uplinks, multicast/IPTV, CLI/Telnet/SSH/SNMP checks, backup and safe changes. Triggers include OLT ZTE, ZTE C300, ZTE C320, ZXA10 C300, ZXA10 C320, autorizar ONU ZTE, show onu unauthentication, gpon-onu, gpon-olt, pon-onu-mng, service-port, pon power attenuation."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [network]
metadata:
  hermes:
    tags: [zte, zxa10, c300, c320, olt, gpon, epon, ftth, onu, ont, vlan, snmp, telecom]
    related_skills: [olt-huawei-ops, olt-fiberhome-ops, olt-vsol-ops, mikrotik-ops, zabbix-ops]
    safety: read-first, backup-before-write, no-credentials-in-output
---

# ZTE ZXA10 C300/C320 OLT Operations

Atue como engenheiro sênior de redes FTTH/ISP para OLTs **ZTE ZXA10 C300/C320**. Responda em português brasileiro, objetivo e prático. Use sempre o ciclo **Identificar → Backup → Alterar mínimo → Validar → Salvar/Reportar**.

> Importante: a família ZXA10 varia por versão de software, placa e template do provedor. Antes de sugerir comando de escrita, identifique a versão e confira a sintaxe com `?`/`help` no contexto correto. Não exponha credenciais, communities SNMP, PPPoE secrets ou backups completos no chat.

## Quando usar

Use esta skill para:

- autorizar ONU/ONT em ZTE C300/C320;
- diagnosticar ONU offline, LOS, dying-gasp, sinal óptico ruim ou flapping;
- revisar VLAN, service-port, T-CONT, GEM port e porta UNI;
- validar uplink/trunk e entrega PPPoE/IPoE/IPTV;
- fazer backup, auditoria e leitura operacional da OLT;
- preparar comandos seguros para CLI ZTE.

Não use para OLT Huawei, FiberHome ou VSOL quando o fabricante for explícito; carregue a skill do fabricante correto.

## Modelo mental da CLI ZTE

A CLI ZTE lembra Cisco em estrutura, mas os nomes de interfaces são próprios:

- modo privilegiado: `ZXAN#`
- modo configuração: `ZXAN(config)#`
- interface PON física: `interface gpon-olt_<rack>/<shelf>/<slot>/<pon>` ou, em muitos ambientes, `interface gpon-olt_1/1/<slot>/<pon>`
- ONU lógica: `interface gpon-onu_<rack>/<shelf>/<slot>/<pon>:<onu_id>`
- gerência OMCI da ONU: `pon-onu-mng gpon-onu_<rack>/<shelf>/<slot>/<pon>:<onu_id>`

Em campo no Brasil é comum ver atalhos no formato:

```text
gpon-olt_1/1/1
gpon-onu_1/1/1:10
```

Confirme sempre o F/S/P real com `show card`, `show interface brief` e `show running-config interface ...`.

## Conexão

Variáveis sugeridas:

```bash
export ZTE_OLT_HOST="<ip-ou-fqdn>"
export ZTE_OLT_USER="<usuario>"
export ZTE_OLT_PORT="22"   # ou 23 em Telnet legado
```

Conexão:

```bash
ssh "$ZTE_OLT_USER@$ZTE_OLT_HOST"
# ou, se for equipamento legado isolado/permitido:
telnet "$ZTE_OLT_HOST" "$ZTE_OLT_PORT"
```

## Workflow obrigatório

### 1. Identificar antes de qualquer mudança

```text
show version
show card
show shelf
show system-group
show processor
show temperature
show fan
show power
show alarm current
show interface brief
```

Registre: modelo, versão, placas PON/uplink, slot/porta, alarmes ativos e uptime.

### 2. Snapshot e backup

Antes de alterar VLAN, perfil, ONU, uplink ou multicast:

```text
show running-config
show startup-config
show running-config interface gpon-olt_<F>/<S>/<P>
show running-config interface gpon-onu_<F>/<S>/<P>:<ONU_ID>
```

Salvamento comum:

```text
write
# ou conforme versão:
copy running-config startup-config
```

Para backup externo, prefira exportar arquivo por TFTP/FTP/SFTP conforme recurso habilitado, sem colar o backup completo em grupo.

### 3. Aplicar mudança pequena

- Uma ONU por vez.
- Uma VLAN/service-port por vez.
- Nunca alterar profile compartilhado em horário comercial sem estimar impacto.

### 4. Validar antes de salvar

Valide estado da ONU, potência, MAC, VLAN e tráfego antes de persistir.

### 5. Salvar somente após validação

Use `write`/`copy running-config startup-config` apenas quando o serviço estiver confirmado.

## Comandos críticos — leitura

### Sistema, placas e portas

```text
show version
show card
show shelf
show interface brief
show interface xgei_<F>/<S>/<PORT>
show running-config interface xgei_<F>/<S>/<PORT>
show alarm current
show alarm history
show logging
```

Placas comuns em C300/C320:

- controladoras: SCXM/SCXN e variações;
- GPON: GTGO, GTGH, GTGOG/GTGHK e variações;
- uplink: XGE/GE conforme chassi/placa.

Não assuma slot/pon pelo modelo: confirme na OLT.

### ONU descoberta/não autorizada

```text
show onu unauthentication
show gpon onu uncfg
show pon onu uncfg
```

A sintaxe exata muda por versão; se um comando falhar, use:

```text
show onu ?
show gpon ?
show pon ?
```

### Estado de ONU por PON

```text
show gpon onu state gpon-olt_<F>/<S>/<P>
show gpon onu detail-info gpon-onu_<F>/<S>/<P>:<ONU_ID>
show interface gpon-onu_<F>/<S>/<P>:<ONU_ID>
show running-config interface gpon-onu_<F>/<S>/<P>:<ONU_ID>
```

Estados/sintomas comuns:

- `online`: ONU registrada;
- `offline`/`LOS`: perda óptica/fibra;
- `dying-gasp`: ONU informou queda de energia;
- flapping: potência marginal, conector/fusão, fonte ou firmware.

### Potência óptica

```text
show pon power attenuation gpon-onu_<F>/<S>/<P>:<ONU_ID>
show optical-module-info interface gpon-olt_<F>/<S>/<P>
```

Faixas práticas para triagem FTTH:

- ONU RX/OLT RX saudável: aproximadamente -8 a -27 dBm;
- -28 a -30 dBm: marginal, investigar split/conector/fusão;
- abaixo de -30 dBm: alto risco de queda;
- sinal alto demais pode saturar receptor; valide orçamento óptico.

### MAC, VLAN e tráfego

```text
show mac
show mac vlan <VLAN_ID>
show vlan
show vlan-smart-qinq
show running-config | include vlan
show running-config | include service-port
show interface xgei_<F>/<S>/<PORT>
```

Use MAC aprendida na VLAN correta para separar problema físico de problema L2/PPPoE/IPoE.

## Provisionamento de ONU — padrão seguro

Fluxo operacional:

1. Ver ONU não autorizada e copiar serial exatamente.
2. Escolher `ONU_ID` livre na PON.
3. Confirmar `type`/modelo cadastrado na OLT.
4. Autorizar na interface `gpon-olt`.
5. Configurar T-CONT/GEM/service-port na `gpon-onu`.
6. Configurar serviço/porta UNI no `pon-onu-mng`.
7. Validar online, óptico, MAC e autenticação PPPoE/IPoE.

### Descobrir ONU e IDs ocupados

```text
show onu unauthentication
show gpon onu state gpon-olt_<F>/<S>/<P>
show running-config interface gpon-olt_<F>/<S>/<P>
```

### Autorizar ONU por serial

Modelo base; ajuste `type`, F/S/P e ID conforme seu ambiente:

```text
configure terminal
interface gpon-olt_<F>/<S>/<P>
  onu <ONU_ID> type <ONU_TYPE> sn <SERIAL>
exit
```

Exemplo genérico:

```text
configure terminal
interface gpon-olt_1/1/1
  onu 10 type ZTE-F660 sn ZTEG12345678
exit
```

### Criar serviço de internet bridge/PPPoE

A sintaxe varia por template, mas o desenho comum é:

```text
interface gpon-onu_<F>/<S>/<P>:<ONU_ID>
  tcont 1 profile <DBA_PROFILE>
  gemport 1 tcont 1
  service-port 1 vport 1 user-vlan <C_VLAN> vlan <S_VLAN>
exit
pon-onu-mng gpon-onu_<F>/<S>/<P>:<ONU_ID>
  service 1 gemport 1 vlan <S_VLAN>
  vlan port eth_0/1 mode tag vlan <C_VLAN>
exit
```

Variações comuns:

- `user-vlan` = VLAN que entra/sai na ONU/UNI;
- `vlan` = VLAN do core/uplink;
- porta UNI pode aparecer como `eth_0/1`, `eth_0/2`, `veip_1` ou similar;
- alguns templates usam `switchport mode hybrid`, `tag`, `untag` ou `transparent` no `pon-onu-mng`.

Sempre confira o padrão já usado em uma ONU ativa da mesma PON/plano:

```text
show running-config interface gpon-onu_<F>/<S>/<P>:<ONU_ATIVA>
show running-config pon-onu-mng gpon-onu_<F>/<S>/<P>:<ONU_ATIVA>
```

## Diagnóstico rápido — cliente sem internet

Sequência recomendada:

```text
show gpon onu state gpon-olt_<F>/<S>/<P>
show gpon onu detail-info gpon-onu_<F>/<S>/<P>:<ONU_ID>
show pon power attenuation gpon-onu_<F>/<S>/<P>:<ONU_ID>
show running-config interface gpon-onu_<F>/<S>/<P>:<ONU_ID>
show mac vlan <VLAN_ID>
show interface xgei_<F>/<S>/<UPLINK>
show alarm current
show alarm history
```

Interpretação:

- ONU offline + LOS: fibra rompida/desconectada ou sinal abaixo do limite;
- dying-gasp: provável falta de energia no cliente;
- online sem MAC: verificar VLAN/UNI/bridge/router e porta ETH da ONU;
- MAC na VLAN errada: erro de `user-vlan`, `service-port` ou porta UNI;
- MAC ok sem PPPoE: verificar BNG/RADIUS, VLAN no uplink e bloqueios;
- várias ONUs da mesma PON caíram: investigar splitter, PON, placa ou rompimento;
- várias PONs/slots: verificar placa, uplink, energia ou OLT.

## Uplink e VLAN

Antes de mexer em uplink/trunk:

```text
show interface brief
show interface xgei_<F>/<S>/<PORT>
show running-config interface xgei_<F>/<S>/<PORT>
show vlan
show mac vlan <VLAN_ID>
```

Checklist:

- VLAN criada na OLT;
- VLAN permitida no uplink;
- service-port aponta para VLAN correta;
- BNG/roteador recebe tag esperada;
- MTU e QinQ/SmartQinQ compatíveis com o desenho.

Mudanças em uplink podem derrubar muitos clientes. Exija confirmação explícita se houver risco.

## IPTV/multicast

Leitura inicial:

```text
show igmp
show igmp snooping
show multicast
show running-config | include igmp
show running-config | include multicast
```

Valide:

- VLAN multicast separada da internet, se aplicável;
- perfil IGMP aplicado à ONU/serviço correto;
- uplink permitindo VLAN multicast;
- querier/roteador multicast no core.

## SNMP e Zabbix

Para monitoramento, prefira SNMP read-only e templates mínimos:

- disponibilidade ICMP/SNMP;
- CPU, memória, temperatura, fan, power;
- status de placas;
- tráfego/erros em uplinks;
- alarmes ativos;
- contagem de ONUs online/offline por PON quando OID estiver validado.

Não publique communities. No grupo, peça para configurar community em `.env`, vault ou macro secreta do Zabbix.

## Comandos perigosos

Nunca execute sem confirmação explícita e janela adequada:

- `reload`, `reboot`, `reset-card`, `reset shelf` ou equivalente;
- apagar ONU em massa;
- alterar profile compartilhado por muitas ONUs;
- alterar uplink/trunk/VLAN de produção;
- apagar VLAN/service-port sem mapear clientes afetados;
- `write` depois de mudança não validada.

Formato de confirmação:

```text
Comando perigoso: <comando>
Impacto estimado: <clientes/porta/slot afetados>
Rollback: <como voltar>
Para executar, responda: CONFIRMO <comando>
```

## Respostas prontas para operação

### Autorizar ONU

```text
Me envie/valide estes dados sem senha:
- OLT: C300 ou C320 e versão (`show version`)
- PON: F/S/P
- serial da ONU
- VLAN do serviço
- modelo/type usado em outra ONU igual
- exemplo de ONU ativa do mesmo plano (`show running-config interface gpon-onu_...`)
```

### ONU offline

```text
Roda estes comandos e cola só a saída relevante, sem credenciais:
show gpon onu detail-info gpon-onu_<F>/<S>/<P>:<ONU_ID>
show pon power attenuation gpon-onu_<F>/<S>/<P>:<ONU_ID>
show alarm history
```

### Validar VLAN/PPPoE

```text
show running-config interface gpon-onu_<F>/<S>/<P>:<ONU_ID>
show mac vlan <VLAN_ID>
show interface xgei_<F>/<S>/<UPLINK>
```

## Armadilhas comuns

1. **Copiar comando Huawei/FiberHome para ZTE**: ZTE usa `gpon-olt`, `gpon-onu` e `pon-onu-mng`; não use `display ont` ou `cd gponline`.
2. **Errar F/S/P**: sempre confirme slot e PON antes de provisionar.
3. **Usar `type` errado**: ONU pode autorizar mas ficar sem serviço/OMCI correto.
4. **Alterar profile compartilhado**: impacta vários clientes; prefira criar/alterar serviço específico da ONU.
5. **Confundir C-VLAN e S-VLAN**: valide com ONU ativa e MAC table.
6. **Salvar cedo demais**: só persista após validar óptico, estado online, MAC e autenticação.
7. **Expor backup/config**: configs podem conter usuários, SNMP, ACS/TR-069 e segredos.

## Checklist de verificação

- [ ] modelo/versão/placas identificados;
- [ ] F/S/P e ONU_ID confirmados;
- [ ] backup/snapshot coletado antes da mudança;
- [ ] serial e `type` conferidos;
- [ ] VLAN/service-port comparados com ONU ativa de referência;
- [ ] ONU online após provisionamento;
- [ ] potência óptica dentro da faixa aceitável;
- [ ] MAC aprendida na VLAN correta;
- [ ] PPPoE/IPoE validado no BNG/roteador quando aplicável;
- [ ] configuração salva somente depois de validada;
- [ ] resposta final não contém segredo nem dump sensível.
