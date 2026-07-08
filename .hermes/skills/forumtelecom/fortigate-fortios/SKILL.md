---
name: fortigate-fortios
description: "Senior Fortinet FortiGate/FortiOS firewall engineer. Use when the user asks to diagnose, configure, audit, or troubleshoot FortiGate/FortiOS 7.4/7.6: CLI, interfaces, routing, firewall policies, NAT, IPsec/SSL VPN, SD-WAN, UTM/security profiles, HA, FortiLink/FortiSwitch, FortiAnalyzer/syslog logging, FortiGuard, and diagnose debug flow/sniffer."
version: 1.0.0
author: Hermes Agent / Forum Telecom
license: MIT
platforms: [fortios, linux]
metadata:
  hermes:
    tags: [fortigate, fortios, fortinet, firewall, vpn, sd-wan, ha, utm]
    related_skills: [opnsense-ops, cisco-ops, mikrotik-ops]
    source_research:
      - https://docs.fortinet.com
      - https://community.fortinet.com
      - https://www.fortiguard.com
---
# FortiOS / FortiGate — Administração e Troubleshooting

Skill de referência para administradores de firewalls Fortinet FortiGate no Brasil.
Cobre FortiOS 7.4 e 7.6, com comandos reais do CLI, fluxos de troubleshooting
e referências à documentação oficial Fortinet.

## Contract

Esta skill garante:
- Comandos CLI reais e sintaticamente corretos do FortiOS
- Referências à documentação oficial (docs.fortinet.com, Fortinet Cookbook)
- Fluxo estruturado de troubleshooting (sintoma → diagnose → fix)
- Awareness de armadilhas comuns (policy order, HA split-brain, SD-WAN SLA stickiness)
- Respostas em português brasileiro para admins no Brasil


## Segurança obrigatória

- Operar em modo leitura por padrão; mudanças em produção exigem confirmação clara do escopo.
- Nunca publicar PSK, senha, token, backup completo, serial privado ou configuração real de cliente.
- Antes de alterar firewall policy, VPN, SD-WAN, HA ou UTM: coletar snapshot/backup e plano de rollback.
- Comandos destrutivos como factory reset, reboot, upgrade e kill de processo só com confirmação explícita e janela de manutenção.

## 1. CLI Básico

### Comandos essenciais

```
get system status                          # Versão firmware, serial, uptime, hostname
get system performance status              # CPU, memória, sessões ativas, throughput
execute update-now                         # Força update manual (FortiGuard, certificados)
config system global
  set hostname "FW-CORP"
  set timezone 03                          # Brasília (GMT-3)
  set admin-sport 443
  set admin-ssh-port 22
end
get system admin                           # Lista administradores configurados
# execute factoryreset                     # DESTRUTIVO: só com confirmação explícita e janela de manutenção
```

### Referência oficial
- **FortiOS 7.4/7.6 CLI Reference** — Seção *System Settings*
- **FortiOS 7.4/7.6 Administration Guide** — Capítulo *System Settings*

## 2. Interfaces e Roteamento

### Comandos essenciais

```
get system interface                       # Lista interfaces com IP, status e estatísticas
config system interface
  edit "port1"
    set alias "WAN1"
    set mode static
    set ip 203.0.113.10 255.255.255.0
    set allowaccess ping https ssh fgfm
  next
end

get router info routing-table all          # Tabela de roteamento completa
config router static
  edit 1
    set dst 10.0.0.0 255.0.0.0
    set gateway 192.168.1.1
    set device "port2"
  next
end

get router info ospf neighbor              # Adjacências OSPF
config router ospf
  set router-id 1.1.1.1
  config area
    edit 0.0.0.0
      config interface
        edit "port2"
          set network-type broadcast
        next
      end
    next
  end
end

config router bgp
  set as 65001
  set router-id 1.1.1.1
  config neighbor
    edit "10.0.0.1"
      set remote-as 65002
    next
  end
end

execute ping 8.8.8.8
execute traceroute 8.8.8.8
```

### Referência oficial
- **FortiOS 7.4/7.6 Administration Guide** — Capítulos *Network Interfaces* e *Routing*
- **FortiOS 7.4/7.6 CLI Reference** — Seções `config system interface` / `config router`

## 3. Firewall Policies

### Comandos essenciais

```
get firewall policy                        # Lista todas as policies
show firewall policy                       # Configuração completa das policies
get firewall policy filter                 # Filtra policies por critérios

config firewall policy
  edit 10
    set name "LAN-to-WAN-Allow"
    set srcintf "port2"
    set dstintf "port1"
    set srcaddr "all"
    set dstaddr "all"
    set action accept
    set schedule "always"
    set service "ALL"
    set utm-status enable
    set ssl-ssh-profile "certificate-inspection"
    set av-profile "default"
    set webfilter-profile "default"
    set logtraffic all
    set nat enable
  next
end

config firewall address
  edit "SERVER-WEB"
    set subnet 10.0.0.10/32
  next
end

config firewall service custom
  edit "TCP-8443"
    set tcp-portrange 8443
  next
end

diagnose firewall iprope list              # Policies internas do kernel
diagnose debug flow filter                 # Filtra fluxos para debug de policy match
diagnose debug flow show function-name enable
diagnose debug start
```

> **Pitfall:** Policies são avaliadas de cima para baixo (menor ID primeiro).
> Sempre posicionar políticas mais específicas ACIMA das genéricas.
> `diagnose firewall iprope list` mostra a ordem real avaliada pelo kernel.

### Referência oficial
- **FortiOS 7.4/7.6 Administration Guide** — Capítulo *Firewall Policies*
- **FortiOS 7.4/7.6 CLI Reference** — Seção `config firewall policy`

## 4. VPN IPsec e SSL

### IPsec

```
get vpn ipsec tunnel list                  # Túneis IPsec e status
diagnose vpn tunnel list                   # Detalhes dos túneis ativos
diagnose vpn ike gateway list              # Estado IKE detalhado

config vpn ipsec phase1-interface
  edit "VPN-BRANCH"
    set interface "port1"
    set peertype any
    set net-device enable
    set proposal aes256-sha256 aes128-sha256
    set remote-gw 198.51.100.5
    set psksecret <PSK_SECRET>              # nunca publique a PSK em chat/repositório
    set dpd on-idle
    set dpd-retryinterval 10
  next
end

config vpn ipsec phase2-interface
  edit "VPN-BRANCH"
    set phase1name "VPN-BRANCH"
    set proposal aes256-sha256
    set src-subnet 10.0.0.0 255.0.0.0
    set dst-subnet 172.16.0.0 255.240.0.0
  next
end

diagnose debug application ike -1          # Debug completo IKE
diagnose debug enable
```

### SSL VPN

```
get vpn ssl stats                          # Estatísticas de sessões SSL VPN
diagnose vpn ssl session list              # Sessões SSL VPN ativas

config vpn ssl settings
  set port 443
  set tunnel-ip-pools "SSLVPN_TUNNEL_ADDR1"
  set source-interface "port1"
  set source-address "all"
  set default-portal "full-access"
  set auth-timeout 28800
end

config vpn ssl web portal
  edit "portal-remoto"
    set tunnel-mode enable
    set ip-pools "SSLVPN_TUNNEL_ADDR1"
    set split-tunneling enable
    set split-tunneling-routing-address "LAN-Subnets"
  next
end

config vpn ssl web user-group-bookmark
  edit "portal-remoto"
    config bookmarks
      edit "Intranet"
        set url "https://10.0.0.100"
      next
    end
  next
end
```

### Referência oficial
- **FortiOS 7.4/7.6 Administration Guide** — Capítulos *IPsec VPN* e *SSL VPN*
- **FortiOS 7.4/7.6 CLI Reference** — Seções `config vpn ipsec` / `config vpn ssl`

## 5. SD-WAN

### Comandos essenciais

```
get system sdwan health-check              # Status dos health checks
get system sdwan service                   # Regras de serviço SD-WAN
diagnose sys sdwan health-check            # Resultado detalhado dos probes
diagnose sys sdwan service                 # Seleção de membro por serviço
diagnose sys sdwan sla-log                 # Histórico de SLA

config system sdwan
  set status enable
  config zone
    edit "WAN"
      set service-sla-stickiness enable
    next
  end

  config members
    edit 1
      set interface "port1"
      set gateway 203.0.113.1
      set priority 1
      set cost 5
    next
    edit 2
      set interface "port2"
      set gateway 203.0.113.2
      set priority 2
      set cost 10
    next
  end

  config health-check
    edit "ping-google"
      set server 8.8.8.8
      set members 1 2
      set sla-pass-enable enable
      set sla-fail-enable enable
    next
  end

  config service
    edit 1
      set name "Critical-Traffic"
      set mode sla
      set src "all"
      set dst "all"
      set priority-members 1
      config sla
        edit "ping-google"
          set id 1
          set latency 300
          set jitter 50
          set packetloss 3
        next
      end
    next
  end
end
```

> **Pitfall:** `service-sla-stickiness` mantém sessões no membro original mesmo
> quando SLA falha brevemente. Em links instáveis, isso evita flap mas pode
> manter tráfego em link ruim por até 30s. Ajustar conforme SLA do contrato.

### Referência oficial
- **FortiOS 7.4/7.6 Administration Guide** — Capítulo *SD-WAN*
- **FortiOS 7.4/7.6 SD-WAN Cookbook** (cookbook.fortinet.com)

## 6. UTM / Security Profiles

### Comandos essenciais

```
get antivirus profile                      # Perfis de antivírus
get ips sensor                             # Sensores IPS
get webfilter profile                      # Perfis de web filter
get application list                       # Perfis de controle de aplicação

config ips sensor
  edit "protecao-completa"
    set comment "Perfil IPS para servidores críticos"
    set scan-mode tunnel
    config entries
      edit 1
        set action reset
        set location all
        set os all
        set protocol all
        set service all
        set status enable
      next
    end
  next
end

config webfilter profile
  edit "bloqueio-social"
    set comment "Bloqueia redes sociais"
    set ftgd-wf
      config filters
        edit 1
          set category-id 57               # Social Networking
          set action block
        next
      end
    end
  next
end

config dnsfilter profile
  edit "safe-search"
    set ftgd-dns
      config filters
        edit 1
          set category-id 57
          set action block
        next
      end
    end
  next
end

diagnose test application ips 9999         # Reinicia motor IPS (cuidado em produção!)
diagnose sys top                           # Processos UTM consumindo CPU
```

### Referência oficial
- **FortiOS 7.4/7.6 Administration Guide** — Capítulo *Security Profiles*
- **FortiOS 7.4/7.6 CLI Reference** — Seções `config antivirus`, `config ips`, `config webfilter`
- **FortiGuard Labs** — https://www.fortiguard.com (threat intelligence)

## 7. High Availability (HA)

### Comandos essenciais

```
get system ha status                       # Status HA, master/slave, sync
get system ha diagnostics                  # Diagnóstico detalhado do cluster
diagnose sys ha dump-csum                  # Checksum de configuração (sync)
diagnose sys ha checksum cluster           # Compara checksums entre nós
execute ha manage-backup                   # Acessa console do slave

config system ha
  set group-name "CLUSTER-FW"
  set mode a-p                             # active-passive (a-a para active-active)
  set hbdev "ha1" 50 "ha2" 50              # Interfaces heartbeat
  set session-pickup enable
  set session-pickup-connectionless enable
  set override enable
  set priority 200                         # Prioridade deste membro
  set unicast-enable enable                # HA unicast (evita broadcast)
  set monitor "port1" "port2"              # Monitora interfaces para failover
end

diagnose sys session list                  # Sessões sincronizadas
```

> **Pitfall (Split-brain):** Sem `unicast-enable` em redes com switches que
> bloqueiam broadcast/multicast entre VLANs, os nós perdem heartbeat e ambos
> viram master. Sempre usar HA unicast em ambientes virtualizados ou com
> segmentação L2 rigorosa.

### Referência oficial
- **FortiOS 7.4/7.6 Administration Guide** — Capítulo *High Availability*
- **FortiOS 7.4/7.6 High Availability Troubleshooting** (Fortinet Document Library)

## 8. Troubleshooting

### Comandos essenciais

```
diagnose debug enable
diagnose debug flow filter addr <IP>
diagnose debug flow show function-name enable
diagnose debug flow show console enable
diagnose debug start
diagnose debug stop
diagnose debug reset

diagnose sniffer packet <intf> 'host <IP>' 4   # Sniffer (tcpdump-like)
execute ping <IP>
execute traceroute <IP>

diagnose sys top                               # Top de processos (CPU/MEM)
diagnose sys top-summary                       # Resumo geral do sistema
diagnose sys kill 11 <PID>                     # Interrompe processo travado; validar impacto antes

diagnose sys session list                      # Sessões ativas
diagnose sys session filter <filtro>
diagnose sys session ttl

diagnose hardware sysinfo memory
diagnose hardware sysinfo flash
diagnose sys info
```

### Fluxo estruturado de debug de policy

1. Identificar IP/porta/protocolo do fluxo problemático
2. `diagnose debug flow filter addr <IP>` + `diagnose debug flow filter port <porta>`
3. `diagnose debug flow show function-name enable`
4. `diagnose debug start` e reproduzir o tráfego
5. Ler no console qual policy ID fez match (ou se foi `iprope_deny` — drop implícito)
6. `diagnose debug reset` ao terminar (sempre!)

> **Pitfall:** Esquecer de dar `diagnose debug reset` depois do teste deixa o
> FortiGate logando TODOS os pacotes — em produção isso pode travar o appliance
> em minutos por overload de CPU/IO.

### Referência oficial
- **FortiOS 7.4/7.6 Troubleshooting Guide** (docs.fortinet.com)
- **FortiOS 7.4/7.6 CLI Reference** — Seção `diagnose`
- **Fortinet Community: Troubleshooting Tips** (community.fortinet.com)

## 9. FortiLink / FortiSwitch

### Comandos essenciais

```
get switch-controller managed-switch       # Switches gerenciados via FortiLink
get switch-controller global               # Configuração global FortiLink
diagnose switch-controller discovery-info  # Switches em descoberta
execute switch-controller get-conn-status  # Status das conexões FortiLink

config switch-controller global
  set fortilink enable
  set allow-access https ping ssh
  set default-vlan "default"
  set https-image-replace enable
end

config switch-controller managed-switch
  edit "S248DN2023000001"                  # Serial do switch
    set fsw-wan1-peer "fortilink"
    config ports
      edit "port1"
        set vlan "LAN"
        set allowed-vlans "VOICE" "DATA"
        set speed auto
        set status enable
      next
    end
  next
end

config switch-controller network
  edit "VOICE"
    set vlan-id 200
    set interface "port1"
  next
end

diagnose switch-controller interface show
execute switch-controller restart-arp
```

### Referência oficial
- **FortiOS 7.4/7.6 Administration Guide** — Capítulo *Switch Controller (FortiLink)*
- **FortiSwitch 7.4/7.6 Administration Guide**
- **FortiOS 7.4/7.6 CLI Reference** — Seção `config switch-controller`

## 10. Logging

### Comandos essenciais

```
get log memory setting                     # Configurações de log em memória
get log disk setting                       # Configurações de log em disco
get log fortianalyzer setting              # Conexão com FortiAnalyzer
diagnose debug application syslogd -1      # Debug do daemon syslog
diagnose log test                          # Log de teste para validar envio
diagnose sys log rate                      # Taxa de logs por segundo
get log info                               # Storage de log

config log syslogd setting
  set status enable
  set server "10.0.0.100"
  set port 514
  set reliable enable
end

config log fortianalyzer setting
  set status enable
  set server "10.0.0.200"
  set upload-option realtime
  set upload-interval 5
  set source-ip "10.1.1.1"
end

config log setting
  set local-in-allow enable                # Loga tráfego para o FortiGate
  set local-out enable                     # Loga tráfego originado pelo FortiGate
  set daemon-log enable
end

execute log filter
execute log display
```

### Referência oficial
- **FortiOS 7.4/7.6 Administration Guide** — Capítulo *Logging and Reporting*
- **FortiOS 7.4/7.6 Log Message Reference** (docs.fortinet.com)
- **FortiAnalyzer 7.4/7.6 Administration Guide** (para integração)

## Dicionário Rápido de Comandos

| Comando | Descrição |
|---------|-----------|
| `?` ou `<tab>` | Auto-complete e ajuda no CLI |
| `show` | Exibe configuração salva (não runtime) |
| `show full-configuration` | Exibe TODA a config incluindo padrões |
| `get` | Exibe status em tempo real (runtime) |
| `diagnose` | Diagnóstico avançado e debug |
| `execute` | Executa ações (backup, update, reboot) |
| `config` | Entra no modo de configuração |
| `end` | Sai do modo config e **salva** alterações |
| `abort` | Sai do modo config **sem salvar** |
| `next` | Avança para próximo item em lista config |
| `edit <id>` | Cria ou edita item específico |

## Anti-Patterns

- ❌ Usar `diagnose debug enable` sem dar `diagnose debug reset` depois — trava produção.
- ❌ Colocar policy genérica acima de específica — a ordem é avaliada top-down.
- ❌ HA sem `unicast-enable` em ambientes com L2 segmentado — causa split-brain.
- ❌ SD-WAN sem health-check configurado — service nunca muda de membro.
- ❌ Apontar DNS do FortiGate para si mesmo antes de ter DNS interno configurado.
- ❌ Esquecer `set logtraffic all` em policies críticas — sem log, sem auditoria.
- ❌ Reiniciar motor IPS (`diagnose test application ips 9999`) em horário de pico.
- ❌ Não habilitar SSL inspection em policy com UTM — AV/WebFilter não inspecionam HTTPS.

## Output Format

Ao responder sobre FortiGate/FortiOS:

1. Confirmar versão do FortiOS e modelo (se relevante para o comando).
2. Fornecer comandos CLI executáveis com sintaxe correta.
3. Indicar referências da documentação oficial Fortinet.
4. Alertar sobre pitfalls específicos daquele cenário.
5. Se troubleshooting, seguir o fluxo estruturado (debug flow → policy match → fix).

## Links Úteis da Documentação Oficial

| Recurso | URL |
|---------|-----|
| Fortinet Document Library | https://docs.fortinet.com |
| FortiOS 7.4 Release Notes | https://docs.fortinet.com/document/fortigate/7.4.0/release-notes |
| FortiOS 7.6 Release Notes | https://docs.fortinet.com/document/fortigate/7.6.0/release-notes |
| Fortinet Community | https://community.fortinet.com |
| Fortinet Knowledge Base (KB) | https://kb.fortinet.com |
| Fortinet Training (NSE) | https://training.fortinet.com |
| FortiGuard Labs | https://www.fortiguard.com |
| Fortinet Cookbook | https://cookbook.fortinet.com |

## Ferramentas e Referências

- `diagnose debug flow` — Debug de policy match (principal ferramenta de troubleshooting)
- `diagnose sniffer packet` — Captura de pacotes estilo tcpdump
- `diagnose sys top` — Monitor de processos (CPU/MEM)
- `diagnose vpn ike gateway list` — Estado IKE detalhado
- `diagnose sys ha checksum cluster` — Validação de sync HA
- **FortiExplorer** — App mobile para console via USB
- **FortiManager** — Gestão centralizada multi-FortiGate
- **FortiAnalyzer** — SIEM/Logging centralizado

*Compilado para FortiOS 7.4 / 7.6 — Junho 2026*
*Público-alvo: Administradores FortiGate no Brasil*
