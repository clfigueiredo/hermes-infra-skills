# Troubleshooting ONU FiberHome — guia prático

## Fluxograma básico

```
Cliente reporta sem internet
    ↓
1. ONU aparece em show authorization?
    NÃO → vai direto para "ONU não descoberta"
    SIM → vai para passo 2
    ↓
2. ONU online em show onu_state?
    NÃO → vai para "ONU offline"
    SIM → vai para passo 3
    ↓
3. RX ótico OK? (acima de -28 dBm)
    NÃO → problema de fibra
    SIM → vai para passo 4
    ↓
4. VLAN configurada no service?
    NÃO → reaplicar service profile
    SIM → vai para passo 5
    ↓
5. Cliente autenticando RADIUS?
    NÃO → problema de PPPoE/credentials
    SIM → problema é cliente-side
```

## Caso 1: ONU não descoberta

```
cd gponline
show discovery slot <X> pon <Y>
```

Se não aparece nada:
- Problema de fibra (corte, conector solto, fusão ruim)
- ONU desligada ou queimada
- PON port da OLT desabilitada (`show pon-port slot <X> pon <Y>`)

## Caso 2: ONU offline (LOS / Dying gasp)

```
cd gponline
show onu_state slot <X> pon <Y>
```

Saída comum:
- `online` — OK
- `offline` — sem comunicação (fibra ou ONU)
- `los` — Loss of Signal
- `auth_failed` — SN ou whitelist errada

LOS = fibra com problema. Verificar:
- RX da OLT vindo da ONU
- Conectores
- Distância (G-PON max 20km com split 1:128)

## Caso 3: RX ótico baixo

```
show optic_module slot <X> pon <Y> onu <ID>
```

Esperado:
- OLT TX: +2 a +5 dBm
- OLT RX (recebendo da ONU): -8 a -28 dBm
- ONU TX: 0.5 a +5 dBm
- ONU RX (recebendo da OLT): -8 a -28 dBm

**Se RX da ONU < -28 dBm:** atenuação alta. Causas:
- Conector sujo (limpar com álcool isopropílico + lenço)
- Fusão ruim (refazer)
- Splitter sobrecarregado
- Distância excedida
- Curva da fibra muito fechada
- DROP de fibra danificado

**Se RX da OLT < -28 dBm:** ONU está fraca enviando ou problema na fibra de subida.

## Caso 4: ONU online mas sem internet

Verificar config service:
```
cd service
show service all
```

Verificar VLAN bind:
```
cd vlan
show pon attach slot <X> pon <Y>
```

Se VLAN OK, problema é PPPoE/RADIUS:
```
show authorization slot <X> pon <Y>
```

Cliente autenticando? Verificar logs de sessão no servidor RADIUS / sistema de gestão.

## Caso 5: ONU online mas Wi-Fi do cliente ruim

Se a ONU é roteada (com Wi-Fi):
```
cd gponline
show onu_info slot <X> pon <Y> onu <ID>
```

Não dá pra mexer no Wi-Fi via OLT diretamente em AN5516 (precisa do ANM2000 ou TL1). Direcionar para reset da ONU pelo cliente (botão físico) ou trocar para padrão se cliente esqueceu senha.

## Sinais óticos por situação

| RX ONU (dBm) | Status |
|---|---|
| -8 a -18 | Excelente |
| -18 a -25 | Bom |
| -25 a -28 | Limítrofe — monitorar |
| < -28 | Ruim — agendar visita técnica |
| `LOS` | Sem sinal — emergência |

## Tipos de ONU comuns no BR e seus IDs em FH

| Modelo | Type ID típico | Modo |
|---|---|---|
| AN5506-04-FA | 26 | Router |
| AN5506-04-FAT | 26 | Router |
| AN5506-01-A | 25 | Bridge |
| BDCOM 3rd-party | 256 | Variável |
| Multilaser ONU | 256 | Bridge usual |
| Nokia 3rd-party | 256 | Variável |

`show onu_type` lista todos os tipos cadastrados na sua OLT.

## Comandos diagnósticos rápidos (cola)

```
cd gponline

# Top 5 ONUs com pior RX no PON (encontrar problemas de fibra)
show optic_module slot <X> pon <Y> | sort -k4

# ONUs descobertas há mais tempo (potenciais problemas)
show discovery

# Reset de ONU específica (NÃO REBOOTA — só faz reauth)
reset onu slot <X> pon <Y> onu <ID>

# Histórico de up/down
show onu_history slot <X> pon <Y> onu <ID>
```
