# Huawei VRP — Cheatsheet rápido

## Diferenças vs Cisco que pegam todo mundo

| O que faz | Cisco | Huawei VRP |
|---|---|---|
| Mostrar config | `show running-config` | `display current-configuration` |
| Mostrar interface | `show interfaces` | `display interface` |
| Mostrar versão | `show version` | `display version` |
| Mostrar rotas | `show ip route` | `display ip routing-table` |
| Mostrar BGP | `show ip bgp summary` | `display bgp peer` |
| Entrar em config | `configure terminal` | `system-view` |
| Sair de config | `end` | `quit` (várias vezes) ou `return` |
| Salvar config | `write memory` | `save` |
| Negar comando | `no <cmd>` | `undo <cmd>` |
| Pipe filter | `\| include` | `\| include` (igual) |
| Habilitar interface | `no shutdown` | `undo shutdown` |
| Description | `description X` | `description X` (igual) |

## Modo de configuração

**V5 (sem commit):**
```
<HW> system-view
[HW] interface GigabitEthernet0/0/0
[HW-GigabitEthernet0/0/0] ip address 10.0.0.1 24
[HW-GigabitEthernet0/0/0] quit
[HW] quit
<HW> save
```

**V8 (com commit):**
```
<HW> system-view
[HW] interface GigabitEthernet0/0/0
[HW-GigabitEthernet0/0/0] ip address 10.0.0.1 24
[HW-GigabitEthernet0/0/0] commit
[HW-GigabitEthernet0/0/0] quit
[HW] quit
<HW> save
```

V8 sem commit = mudança não aplica. Erro mais comum.

## Interface naming

| Cisco | Huawei |
|---|---|
| `GigabitEthernet0/0` | `GigabitEthernet0/0/0` |
| `TenGigabitEthernet0/0/1` | `10GE0/0/1` |
| `HundredGigE0/0` | `100GE0/0/1` |
| `Loopback0` | `LoopBack0` |
| `Vlan100` | `Vlanif100` |

## BGP — sintaxe que pega

**Cisco:**
```
router bgp 65000
 neighbor 10.0.0.1 remote-as 65001
 address-family ipv4
  neighbor 10.0.0.1 activate
```

**Huawei:**
```
bgp 65000
 peer 10.0.0.1 as-number 65001
 ipv4-family unicast
  peer 10.0.0.1 enable
```

## ACL

| Cisco | Huawei |
|---|---|
| `ip access-list standard NAME` | `acl name NAME` |
| `permit ...` | `rule permit ...` |
| `deny ...` | `rule deny ...` |
| `access-class IN in` (vty) | `acl 2000 inbound` (em user-interface) |

## Pipe / filtros úteis

```
display current-configuration | include bgp
display current-configuration | begin interface
display current-configuration | section bgp
display ip routing-table | include 8.8.8.8
```

## Saída de config para arquivo

```
display current-configuration > flash:/backup.cfg
```

## Carregar arquivo de config

```
load configuration flash:/backup.cfg
```

## Comandos VRP-específicos úteis

```
display this                      ! mostra config do view atual
display this | section            ! com seções
return                            ! volta para user-view de qualquer lugar
language-mode chinese / english   ! troca idioma da CLI
screen-length disable             ! sem paginação
mmi-mode enable                   ! modo machine-readable (sem prompts)
```

## Erros comuns ao migrar de Cisco

1. Esquecer `commit` em V8 — config não aplica
2. Usar `show` em vez de `display`
3. Usar `no` em vez de `undo`
4. Usar `configure terminal` em vez de `system-view`
5. Usar `write memory` em vez de `save`
6. Esquecer de usar `LoopBack` (CamelCase) em vez de `Loopback`
7. Em ACL, `rule` é obrigatório antes de `permit/deny`
