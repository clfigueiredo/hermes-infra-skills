# Troubleshooting ONT Huawei MA5800 — guia prático

## Estados de ONT

```
display ont info <slot> <pon> <ont-id>
```

Run state esperado: `online`. Outros valores e o que fazer:

| Run state | Significado | Ação |
|---|---|---|
| `online` | OK | — |
| `offline` | sem comunicação | Verificar fibra |
| `los` | Loss of Signal | Verificar fibra (potência da OLT chegando) |
| `lof` | Loss of Frame | Geralmente fibra ruim ou ONT mal configurada |
| `dying-gasp` | ONT enviou mensagem de "estou morrendo" | Queda de energia na ONT (último sinal antes de desligar) |
| `auth-fail` | Autenticação falhou | Verificar SN ou whitelist |
| `config-fail` | Config não aplicou | Erro em line-profile ou srv-profile |

## Fluxograma diagnóstico

```
Cliente sem internet
    ↓
1. ONT online? (display ont info)
    NÃO → ver run state acima
    SIM → passo 2
    ↓
2. RX ótico OK?
    NÃO → fibra
    SIM → passo 3
    ↓
3. Service-port configurado?
    NÃO → criar service-port
    SIM → passo 4
    ↓
4. MAC aprendido na VLAN do cliente?
    NÃO → ONT/CPE não envia tráfego
    SIM → passo 5
    ↓
5. Cliente autenticando RADIUS/PPPoE no concentrador?
    NÃO → problema fora da OLT
    SIM → problema é cliente-side
```

## Caso 1: ONT offline (LOS)

```
display ont info <slot> <pon> <ont-id>
```

`Run state: los`

Causas comuns:
- Fibra cortada / sem luz
- DROP danificado
- Conector sujo no cliente
- ONT desligada/queimada

Verificar TX da OLT:
```
display port info <slot>/<pon>
```

OLT TX deve estar +2 a +5 dBm. Se -ininf, placa pode estar com problema.

## Caso 2: RX baixo da ONT

```
display ont optical-info 0 1 0 <ont-id>
```

| ONT RX (dBm) | Status |
|---|---|
| -8 a -18 | Excelente |
| -18 a -25 | Bom |
| -25 a -28 | Limítrofe |
| < -28 | Ruim |
| `LOS` | Sem sinal |

**Se RX cliente baixo:**
- Limpar conectores (álcool isopropílico + lenço seco)
- Verificar fusões
- Verificar splitter (calcular budget ótico)
- Visita técnica

## Caso 3: ONT online mas service não funciona

Verificar service-port:
```
display service-port port 0/<slot>/<pon>
```

Saída esperada (resumo):
```
INDEX VLAN F/S/P V/E/S TYPE TAG-TRANSFORM RX TX STATE
100   3713 0/1/0 1/1/1 gpon translate    -- -- up
```

Se `STATE` ≠ `up`:
- VLAN errada
- Tag-transform errado
- Multi-service user-vlan não bate com C-VLAN do cliente

Recriar service-port:
```
undo service-port 100
service-port 100 vlan 3713 gpon 0/1/0 ont 1 gemport 1 multi-service user-vlan 100 tag-transform translate
```

## Caso 4: ONT online, service-port up, sem internet

Verificar MAC aprendido:
```
display mac-address service-port 100
```

Se vazio:
- ONT não está enviando tráfego de cliente
- Cliente não conectado na ONT
- ONT em modo bridge mas porta LAN desabilitada

```
interface gpon 0/1
 display ont port state <pon> <ont-id> eth-port all
```

Se `down`, verificar config da ONT (se gerenciada via OMCI):
```
display ont port attribute <pon> <ont-id> eth <port-id>
```

## Caso 5: Cliente intermitente (cai e volta)

```
display ont event 0 <slot> <pon> <ont-id>
```

Procurar padrão:
- `dying-gasp` repetido = problema de energia na casa do cliente
- `los` repetido = fibra com problema (curva, conector)
- `signal-degrade` = atenuação aumentando (fibra deteriorando)

```
display ont register-info 0 <slot> <pon> <ont-id>
```

Verificar tempo médio entre re-registros. Se < 1h, problema sério.

## Comandos úteis em massa

```
# Top 10 ONTs com pior RX (encontrar problemas de fibra)
interface gpon 0/1
 display ont optical-info 0 all
# (pegar a saída e ordenar manualmente ou via script)

# ONTs offline em todo PON específico
display ont info summary 0/1 | include offline

# Histórico de up/down da última semana
display ont register-info 0 1 0 <ont-id>
```

## Tipos de problema vs primeira ação

| Sintoma | Primeira ação |
|---|---|
| Cliente isolado sem net | `display ont info`, ver run state |
| Vários clientes do mesmo PON sem net | Verificar fibra do PON, splitter |
| Vários clientes de slot diferentes sem net | Problema upstream (uplink, VLAN, RADIUS) |
| Lentidão geral | `display cpu`, `display port traffic` |
| Cliente novo não conecta | `display ont autofind`, ver SN |
| Cliente após troca de ONT | Re-autorizar (whitelist nova SN) |
