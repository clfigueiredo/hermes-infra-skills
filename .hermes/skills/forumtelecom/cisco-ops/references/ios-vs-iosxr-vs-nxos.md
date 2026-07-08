# Cisco IOS vs IOS-XR vs NX-OS — Diferenças críticas

## Modelo de configuração

| Aspecto | IOS / IOS-XE | IOS-XR | NX-OS |
|---|---|---|---|
| Commit model | imediato | commit-based | imediato com checkpoints |
| Rollback | `archive` ou `reload in` | `rollback configuration to <id>` | `rollback running-config checkpoint <name>` |
| Save config | `write memory` ou `copy run start` | implícito após commit | `copy run start` |
| Show running | `show running-config` | `show running-config` | `show running-config` |
| Show interface | `show interfaces` | `show interfaces` | `show interface` (singular!) |

## Sintaxe que muda

| O que | IOS/IOS-XE | IOS-XR | NX-OS |
|---|---|---|---|
| BGP summary | `show ip bgp summary` | `show bgp summary` | `show ip bgp summary` |
| BGP neighbors | `show ip bgp neighbors` | `show bgp neighbor` | `show ip bgp neighbors` |
| OSPF neighbors | `show ip ospf neighbor` | `show ospf neighbor` | `show ip ospf neighbor` |
| Interface descrição | `description X` | `description X` | `description X` |
| Negar comando | `no <cmd>` | `no <cmd>` | `no <cmd>` |
| Habilitar feature | sempre on | sempre on | `feature <nome>` (obrigatório!) |

**NX-OS gotcha**: features (BGP, OSPF, HSRP, etc.) precisam ser **habilitadas explicitamente**:
```
feature bgp
feature ospf
feature interface-vlan
feature lacp
```

## Modos de configuração

**IOS / IOS-XE:**
```
enable
configure terminal
interface Gi0/0
 ip address 10.0.0.1 255.255.255.0
end
write memory
```

**IOS-XR:**
```
configure
interface GigabitEthernet0/0/0/0
 ipv4 address 10.0.0.1/24
 commit
end
```

**NX-OS:**
```
configure terminal
interface Ethernet1/1
 ip address 10.0.0.1/24
 no shutdown
end
copy running-config startup-config
```

## VRF — sintaxe diferente

**IOS / IOS-XE:**
```
ip vrf MGMT
 rd 65000:1
!
interface Gi0/0
 ip vrf forwarding MGMT
 ip address 10.0.0.1 255.255.255.0
```

**IOS-XR:**
```
vrf MGMT
 address-family ipv4 unicast
!
interface GigabitEthernet0/0/0/0
 vrf MGMT
 ipv4 address 10.0.0.1/24
```

**NX-OS:**
```
vrf context MGMT
!
interface Ethernet1/1
 vrf member MGMT
 ip address 10.0.0.1/24
```

## Erros comuns ao migrar

1. **NX-OS**: esquecer `feature <nome>` antes de configurar BGP/OSPF
2. **IOS-XR**: esquecer `commit` — config não aplica
3. **IOS-XR**: usar máscara em vez de prefix-length (`/24` em vez de `255.255.255.0`)
4. **NX-OS**: `show interfaces` (plural) não funciona — é `show interface`
5. **IOS-XR**: `write memory` não existe — config é persistente por commit
