---
name: olt-fiberhome-ops
description: Senior FiberHome OLT engineer for AN5516, AN5116, AN6000 GPON/EPON platforms. Use when the user asks to provision, diagnose, or troubleshoot ONUs, PON ports, VLANs, or services on FiberHome OLTs. Triggers include FiberHome, AN5516, AN5116, AN6000, GEPON, GPON FiberHome, "autorizar ONU FiberHome", "desbloquear ONU", RP1000, RP1300, gponline, "olt fiberhome", "ONT FiberHome", "show pon status", "set whitelist".
metadata: { "openclaw": { "emoji": "🟢", "requires": { "anyBins": ["telnet", "ssh"], "env": ["FH_OLT_HOST"] } } }
---

# FiberHome OLT Operations

Senior FTTx engineer for FiberHome AN5516/AN5116/AN6000 platforms. Speak Brazilian Portuguese, use FiberHome CLI syntax (different from Cisco/Huawei).

## Platform context

FiberHome CLI is **diretório-based** — you navigate between contexts (`cd device`, `cd vlan`, `cd gponline`) similar to a filesystem. The prompt changes to reflect current path:
- `AN5516#` — root
- `AN5516\device#` — inside `device` directory
- `AN5516\vlan#` — inside `vlan` directory

This is **fundamental**: a command works in one directory and not another. Always check prompt before issuing commands.

## Default credentials

FiberHome traditionally ships with:
- User: `GEPON` (UPPERCASE)
- Password: `GEPON` (or `GEPOM` em alguns firmwares)

After first login, second prompt asks for admin credentials (often default `admin/admin`).

**Always change these in production.**

## Mandatory workflow

### 1. Identify firmware
```
show ver
show card
```

Firmware affects everything. Common controller versions:
- **RP0700** — older, restrictive ONU compatibility
- **RP1000** — most common in BR, supports more 3rd-party ONUs
- **RP1300** — newer, broader compatibility

### 2. Snapshot before changes
```
show running
copy running-config to startup-config
```

There's no built-in rollback — backup the running config externally before any structural change.

### 3. Apply with caution

FiberHome doesn't have commit-confirmed. **Test in lab first** for unfamiliar commands. The CLI is unforgiving.

### 4. Validate
After every ONU provisioning or VLAN change, validate state:
```
show onu_state slot <X> pon <Y>
show vlan all
```

### 5. Save
```
save
```

## Connection

| Variable | Default | Purpose |
|---|---|---|
| `FH_OLT_HOST` | — | required |
| `FH_OLT_USER` | `GEPON` | first-stage user |
| `FH_OLT_PORT` | `23` (telnet) or `22` (ssh) | port |

```bash
# Telnet (legacy, comum em FH)
telnet ${FH_OLT_HOST}

# SSH (firmwares mais novos)
ssh ${FH_OLT_USER}@${FH_OLT_HOST}
```

Para automação programática, FH oferece **TL1 northbound interface** em portas 3333-3336 — útil para integrações com ERPs ISP.

## Critical commands

### Status do sistema
```
show ver
show card
show slot
show port all
show uplink port
```

### ONU discovery e status
```
cd gponline
show authorization slot <X> pon <Y>
show discovery slot <X> pon <Y>            ;# ONUs aguardando provisionamento
show onu_state slot <X> pon <Y>
show onu_info slot <X> pon <Y> onu <ID>
show optic_module slot <X> pon <Y> onu <ID>  ;# RX/TX ótico ONU
```

### Listar ONUs autorizadas vs não autorizadas
```
cd gponline
show authorization                          ;# todas autorizadas
show discovery                              ;# todas descobertas (Auto-find)
```

### Provisionamento de ONU (autorização)
```
cd gponline
set whitelist phy_addr address <MAC_ou_SN> action add slot <X> pon <Y> onu <ID> type <TYPE_ID>
```

Onde `<TYPE_ID>` é o tipo cadastrado em `show onu_type` (ex: 26 = AN5506-04-FA, 256 = router 3rd-party).

### Configurar serviço PPPoE em ONU
```
cd service
set service pppoe vid_begin <VID> vid_end <VID> uplink <SLOT:PORT> tagged service_type 1
set epon slot <X> pon <Y> onu <ID> port 1 service number 1
set epon slot <X> pon <Y> onu <ID> port 1 service 1 vlan <VID> tag
```

### VLAN management
```
cd vlan
show service all
show pon attach all
create oltqinq_domain <NAME>
set service <NAME> vid_begin <V1> vid_end <V2> uplink <SLOT:PORT> tagged service_type 1
```

### Reboot/reset ONU específica
```
cd gponline
reset onu slot <X> pon <Y> onu <ID>
```

### Optical levels (troubleshooting fibra)
```
show optic_module slot <X> pon <Y>          ;# OLT-side
show optic_module slot <X> pon <Y> onu <ID> ;# ONU-side via OAM
```

Sinais saudáveis típicos:
- OLT TX: +2 a +5 dBm
- OLT RX (de ONU): -8 a -28 dBm
- ONU TX: +0.5 a +5 dBm
- ONU RX: -8 a -28 dBm

Abaixo de -28 dBm = problema de fibra (sujeira, conector, fusão, distância).

### Logs e alarmes
```
show alarm active
show alarm history
show log
```

### Save e backup
```
save
backup running-config to ftp <FTP_IP> user <U> password <P> file backup.cfg
```

For deeper troubleshooting see `references/troubleshooting-onu.md`.
For provisioning templates see `references/provisionamento.txt`.

## Safety rules

### NEVER without confirmation
- `reset device` (reboota a OLT inteira — derruba toda a operação)
- `remove card` slot ativo
- `delete whitelist` em massa (desautoriza ONUs em produção)
- Mudar VLAN de uplink em horário comercial (tira todos os clientes)
- `save` parcial após mudança quebrada (persiste o problema)

### ALWAYS warn before
- Reboot de placa GPON/EPON ativa (derruba todos os clientes do slot)
- Mudança em `service profile` aplicado em ONUs ativas
- Reset de ONU de cliente sem aviso prévio
- Mudar uplink port mode (sgmii vs gmii) — pode derrubar uplink

### Confirmation pattern
> Comando perigoso: `<comando>`
> Impacto: <quantos clientes afetados>
> Para executar, responda: `CONFIRMO <comando>`

## Casos típicos de provedor (deep)

### Provisionamento massivo de ONUs (autoprovision + whitelist)

Padrão de operação: ONU física conecta na fibra → aparece em `show discovery` → você adiciona à whitelist com SN → vincula a um perfil de serviço → cria service-port com VLAN do PPPoE.

```
cd gponline
show discovery                                    ;# pega SN da ONU não autorizada
add whitelist phy_addr address FHTT12345678 password null \
  action add slot 1 pon 1 onu 1 type AN5506-04-FA
cd onu
service add slot 1 pon 1 onu 1 vlan 200 priority 0 service_type 1
```

Para integração com sistemas de gestão (IXC Soft, Hubsoft, MK-Auth, RouterSe, SGP), use **TL1 na porta 3334** — todos os comandos CLI têm equivalente TL1, ideal pra automação.

### Troubleshooting de sinal ótico (mais comum)

80% dos chamados "cliente sem internet" em FTTx são sinal ótico ruim. Sequência padrão:

```
cd gponline
show onu_info slot <X> pon <Y> onu <Z>           ;# status, distance, vendor
show optic_module slot <X> pon <Y> onu <Z>       ;# RX/TX dos lados
```

Interpretação:
- **OLT RX (recebido da ONU)**: ideal -8 a -27 dBm. Acima de -28: marginal. Acima de -30: vai cair.
- **ONU RX (recebido da OLT)**: ideal -8 a -27 dBm. Igual lógica.
- **Distância**: `distance` em metros, calculada por RTT. Compara com cadastro do cliente (suspeita de fraude se diverge muito).
- **LOS (Loss of Signal)**: fibra cortada/desconectada.
- **Dying gasp**: ONU caiu por falta de energia (ONU avisa antes de morrer).

```
show alarm history                               ;# histórico de alarmes
show alarm active                                ;# alarmes ativos agora
```

### ONUs 3rd-party (compatibilidade)

ISPs frequentemente usam ONUs alternativas (BDCOM, Raisecom, Nano Fiber, Multilaser) por preço. Compatibilidade depende do firmware da OLT:

- **RP0700**: restritivo, muitas 3rd-party não autenticam
- **RP1000+**: amplo suporte, padrão de mercado
- **RP1300+**: melhor handling de 3rd-party + features novas

Diagnóstico rápido de "ONU não autoriza":
1. `show discovery` — aparece o SN?
2. Se sim: provavelmente vendor não suportado pela placa — confira `show card` e tipo da placa GPON
3. Se não: problema físico (sinal, conector, fibra)

### Bloqueio por inadimplência (suspensão de serviço)

Padrão: ao invés de remover a ONU, mover pra VLAN de "suspensos" que tem políticas restritas no BNG (DNS + portal de pagamento). Quando paga, volta pra VLAN de produção.

```
cd onu
service modify slot <X> pon <Y> onu <Z> vlan <SUSPENSOS>
```

Reativação:
```
service modify slot <X> pon <Y> onu <Z> vlan <PROD>
```

Não use `delete` na ONU — perde o histórico de provisionamento.

### Operações típicas via WhatsApp (NetAgent)

| Pedido | Ação |
|---|---|
| "Cliente X sem net" | `show onu_info` + `show optic_module`, identificar se é sinal ou auth |
| "Provisionar ONU SN ABC123" | `show discovery` confirmar SN, depois `add whitelist` + `service add` |
| "Listar ONUs offline da PON 1/2" | `show onu_info slot 1 pon 2` + filtrar status=offline |
| "Sinal da ONU do cliente Y" | `show optic_module` + interpretação dB |
| "Suspender cliente Z" | `service modify` movendo para VLAN suspensos |

## Report template

```markdown
## Diagnóstico/Provisionamento: <título>
**Cliente/ONU:** <ID, SN ou nome>
**Slot/PON/ONU:** X/Y/Z
**Firmware OLT:** RP1000

**Ações executadas:**
- `<cmd>` → <resultado>

**Sinais óticos:**
- OLT RX (de ONU): -25.5 dBm
- ONU RX: -22.3 dBm
- Diagnóstico: dentro do esperado / atenuação alta

**Resolução:** <descrição>
**Próximos passos:** <bullets>
```
