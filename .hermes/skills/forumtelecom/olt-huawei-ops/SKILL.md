---
name: olt-huawei-ops
description: Senior Huawei OLT engineer for MA5800, MA5680T, MA5683T, MA5608T, MA5608, EA5800 GPON/EPON platforms. Use when the user asks to provision, diagnose, or troubleshoot ONTs, PON ports, VLANs, or services on Huawei OLTs. Triggers include MA5800, MA5680T, MA5683T, MA5608T, EA5800, MA5800-X7, MA5800-X15, MA5800-X17, "display ont info", "ont add", "service-port", "GPON Huawei", line-profile, ont-srvprofile, "olt huawei", "ONT Huawei", "auto-find ont", "autorizar ONT".
metadata: { "openclaw": { "emoji": "🟠", "requires": { "anyBins": ["telnet", "ssh"], "env": ["HW_OLT_HOST"] } } }
---

# Huawei OLT Operations (MA5800 family)

Senior FTTx engineer for Huawei MA5800/MA5680T/MA5608T/EA5800 platforms. Speak Brazilian Portuguese, use Huawei VRP-style CLI (note: `display` instead of `show`, `undo` instead of `no`).

## Platform context

Huawei OLTs run **VRP-derived CLI** with three modes:
- **User view**: `<OLT-NAME>` — read-only, monitoring
- **Enable view**: `OLT-NAME#` — privileged commands
- **Config view**: `OLT-NAME(config)#` — configuration mode

Plus context-specific views for interfaces:
- `OLT(config-if-gpon-0/1)#` — inside GPON board context

Common platforms in BR market:
- **MA5680T / MA5683T**: chassi grande, legacy mas ainda comum
- **MA5608T**: 19", densidade média
- **MA5800-X2 / X7 / X15 / X17**: linha moderna, V8 software
- **EA5800**: linha mais nova, virtualização carrier-grade

## Default credentials (alterar imediatamente em produção)

User: `root` ou `admin`
Password: `admin@huawei.com` ou `admin123`

## Mandatory workflow

### 1. Identify
```
display version
display board 0
display sysuptime
```

### 2. Snapshot before changes
```
display saved-configuration
save
backup data to ftp <FTP_IP> <USER> <PASS> backup.cfg
```

### 3. Apply with caution

Huawei OLT applies changes immediately (não tem commit-confirmed). Para mudanças de risco, salvar antes E ter plano de rollback claro.

### 4. Validate com `display`
### 5. Save
```
save
```

## Connection

| Variable | Default | Purpose |
|---|---|---|
| `HW_OLT_HOST` | — | required |
| `HW_OLT_USER` | `admin` | user |
| `HW_OLT_PORT` | `22` (ssh) ou `23` (telnet) | port |

```bash
ssh ${HW_OLT_USER}@${HW_OLT_HOST}
# enable mode
enable
# config mode
config
```

## Critical commands

### Sistema
```
display version
display board 0                              ;# slots e cards
display sysuptime
display cpu                                  ;# uso CPU por slot
display memory
display alarm active
display log
display patch-information
```

### Identificação de PON board
```
display board 0
```
Saída comum:
- `H805GPFD`, `H806GPFD` — placas GPON
- `H802GPBD`, `H805GPBD` — placas GPON antigas
- `H801SCUN` — placa de controle
- `H801GICF` — placa uplink

### Discovery e autorização de ONT

#### Listar ONTs aguardando autorização
```
display ont autofind all
display ont autofind slot 0/1
```

#### Autorizar uma ONT específica (modo SN)
```
config
interface gpon 0/1
 ont add 0 <ID> sn-auth "<SN_HEX>" omci ont-lineprofile-id <LP_ID> ont-srvprofile-id <SP_ID> desc "<DESC>"
quit
```

Exemplo prático:
```
ont add 0 1 sn-auth "485754B5FVBB002" omci ont-lineprofile-id 10 ont-srvprofile-id 10 desc "Cliente_Joao"
```

### Status de ONT
```
display ont info 0 1 0 1                    ;# F/S/P + ONT-ID
display ont info summary 0/1                ;# resumo de todas no PON
display ont optical-info 0 1 0 1            ;# RX/TX óticos
display ont version 0 1 0 1
display ont port state 0 1 0 1 eth-port all
display ont wan-info 0/1 0 1                ;# WAN IP da ONT
display ont autofind all                    ;# ONTs descobertas
```

F/S/P = Frame/Slot/Port (geralmente 0/SLOT/PON)

### Troubleshooting — sinais óticos
```
interface gpon 0/1
 display ont optical-info 0 all              ;# todas no PON
```

Saída:
```
ONT Rx power  Tx power  OLT Rx     ONT Temp  Voltage  Current
ID  (dBm)      (dBm)    power(dBm) (C)       (V)      (mA)
4   -23.10     2.30     -24.21     56        3.260    13
```

Interpretação igual à FiberHome:
- `ONT Rx power`: o que a ONT recebe da OLT (sinal descendente)
- `OLT Rx power`: o que a OLT recebe da ONT (sinal ascendente)
- Faixa saudável: -8 a -28 dBm

### Service-port (criar serviço de internet)

```
config
service-port <SERVICE_ID> vlan <SVLAN> gpon 0/1/<PON> ont <ONT_ID> gemport <GEMPORT> multi-service user-vlan <CVLAN> tag-transform translate
```

Exemplo PPPoE com S-VLAN 3713:
```
service-port 100 vlan 3713 gpon 0/1/0 ont 1 gemport 1 multi-service user-vlan 100 tag-transform translate
```

### Listar service-ports
```
display service-port all
display service-port port 0/1/0              ;# por porta GPON
display service-port vlan 3713
```

### Reboot ONT específica
```
interface gpon 0/1
 ont reset 0 1                               ;# slot pon onu
```

### Logs e alarmes
```
display alarm active
display alarm history
display ont event 0 1 0 1                    ;# eventos da ONT específica
display log
```

### MAC table (debugging L2)
```
display mac-address port 0/1/0
display mac-address vlan 3713
display mac-address service-port 100
```

For deeper troubleshooting see `references/troubleshooting-ont.md`.
For provisioning templates see `references/provisionamento.txt`.

## Safety rules

### NEVER without confirmation
- `reboot` (reboota OLT inteira)
- `reset board` em slot ativo
- `service-port batadd` (adição em massa pode causar problemas se errar VLAN)
- `ont delete` em massa
- Mudar VLAN uplink em horário comercial

### ALWAYS warn before
- Reboot de placa GPON (derruba todos os clientes do slot)
- Mudança em line-profile ou srv-profile aplicado em ONTs ativas
- Reset de ONT sem aviso
- `save` após mudança parcial (persiste config quebrada)

### Confirmation pattern
> Comando perigoso: `<comando>`
> Impacto: <quantos clientes afetados>
> Para executar, responda: `CONFIRMO <comando>`

## Casos típicos de provedor (deep)

### Provisionamento de ONT (autoprovision via auto-find)

Fluxo padrão Huawei: ONT física conecta → vai pra fila de "auto-find" → você confirma com SN → vincula a line-profile + srv-profile → cria service-port com VLAN.

```
config
ont autofind enable
display ont autofind all                          ! pega o SN
interface gpon 0/1
ont add 0 1 sn-auth <SN_HEX> omci ont-lineprofile-id 10 \
  ont-srvprofile-id 10 desc "cliente XYZ"
quit
service-port vlan 200 gpon 0/1/0 ont 1 gemport 1 multi-service \
  user-vlan 200 tag-transform translate
```

A combinação `line-profile + srv-profile + service-port` é o que define o serviço entregue. Provedores grandes mantêm dezenas de profiles para diferentes planos:

```
display ont-lineprofile gpon all
display ont-srvprofile gpon all
display traffic-table ip
```

### Troubleshooting de sinal ótico

Mesma lógica do FiberHome, sintaxe diferente:

```
interface gpon 0/<slot>
 display ont optical-info <pon> <ont_id>
quit
display ont info <slot> <pon> <ont_id>            ! status, distance, run-state
display ont alarm-information <slot> <pon> <ont_id>
```

Estados comuns no `run-state`:
- **online**: ok
- **offline**: caiu (verifique alarm: LOS, dying-gasp, LOFi, LCDGi)
- **failing**: instável, oscilando

**Distance** vem em metros — confronta com cadastro do cliente. Diferenças grandes podem indicar fraude (cliente movido sem aviso) ou erro de cadastro.

### Tag-transform: VLAN cliente vs core

Padrão Huawei usa **tag-transform** para reescrever VLAN entre cliente (C-VLAN) e core/uplink (S-VLAN):

| Modo | Comportamento |
|---|---|
| `transparent` | passa VLAN do cliente sem mexer (cliente já manda taggeado) |
| `translate` | C-VLAN → S-VLAN (1:1) |
| `add` | adiciona S-VLAN sobre C-VLAN (Q-in-Q) |
| `default` | aceita untagged, adiciona VLAN |

Q-in-Q é comum quando OLT só transporta L2 e o BNG (NE40, MikroTik) termina PPPoE.

### Localizar cliente por SN (atendimento)

Cliente liga "minha internet caiu". Você tem o SN da ONT no sistema:

```
display ont info by-sn <SN_HEX>                   ! retorna F/S/P + ONT-ID
display ont info <F> <S> <P> <ID>                 ! status detalhado
display ont event 0 <S> <P> <ID>                  ! últimos eventos
interface gpon 0/<S>
 display ont optical-info <P> <ID>                ! RX/TX
```

Se LOS = problema físico. Se sinal ok mas offline = problema de provisionamento ou perfil.

### Operações típicas via WhatsApp (NetAgent)

| Pedido | Ação |
|---|---|
| "ONT SN HWTC123 caiu" | `display ont info by-sn` + `display ont alarm` |
| "Provisionar nova ONT" | `display ont autofind` + `ont add` com profile |
| "Mover cliente pra VLAN suspensos" | `service-port` modificação ou novo |
| "Sinal de fibra do cliente" | `display ont optical-info` interpretado |
| "Quantas ONTs offline na PON 1/2" | `display ont info 0 2 all` filtrado |

## Report template

```markdown
## Diagnóstico/Provisionamento: <título>
**Cliente/ONT:** <SN ou descrição>
**F/S/P:** 0/1/0 ONT-ID 1
**Plataforma:** MA5800-X7

**Comandos:**
- `<cmd>` → <resultado>

**Sinais óticos:**
- ONT RX (cliente): -23.1 dBm
- OLT RX (de ONT): -24.2 dBm
- Diagnóstico: dentro do esperado / atenuação alta

**Resolução:** <descrição>
**Próximos passos:** <bullets>
```
