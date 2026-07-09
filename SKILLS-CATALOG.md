# Catálogo de Skills Hermes

Página gerada a partir de todos os `SKILL.md` deste repositório. Use como guia rápido para escolher, instalar e acionar cada skill.

## Instalação

Instalar todas as skills:

```bash
git clone https://github.com/clfigueiredo/hermes-infra-skills.git
cd hermes-infra-skills
mkdir -p ~/.hermes/skills
cp -a .hermes/skills/forumtelecom ~/.hermes/skills/
cp -a .hermes/skills/curso-hermes ~/.hermes/skills/
```

Instalar só as skills do curso/alunos:

```bash
mkdir -p ~/.hermes/skills
cp -a .hermes/skills/curso-hermes ~/.hermes/skills/
```

Instalar só as skills de infraestrutura/telecom:

```bash
mkdir -p ~/.hermes/skills
cp -a .hermes/skills/forumtelecom ~/.hermes/skills/
```

Depois, dentro do Hermes:

```text
/reload-skills
```

ou reinicie a sessão/gateway.

## Como usar uma skill

Dentro do Hermes, carregue explicitamente quando quiser garantir o comportamento:

```text
/skill nome-da-skill
```

Exemplo:

```text
/skill security-review-webapp
Revise meu projeto antes de publicar.
```

O Hermes também pode carregar skills automaticamente quando a descrição da tarefa combina com a skill instalada.

## Visão geral

| Pasta | Quantidade | Finalidade |
|---|---:|---|
| `curso-hermes/` | 11 | Skills operacionais para alunos: vibe coding, desenvolvimento, segurança, testes, deploy, GitHub e MCP. |
| `forumtelecom/` | 28 | Skills operacionais para infraestrutura, redes, telecom, virtualização, firewall, monitoramento e sistemas. |

## Índice rápido

| Skill | Pasta | Para que serve |
|---|---|---|
| [`backend-api-patterns`](#backend-api-patterns) | `curso-hermes/` | Use quando o aluno estiver criando ou revisando backend/API. Cobre rotas REST, camada service/repository, validação, erros HTTP, autenticação, rate limit, paginação, logs e contrato entre frontend/backend. |
| [`caveman-terse-mode`](#caveman-terse-mode) | `curso-hermes/` | Use quando o aluno quiser reduzir tokens/verbosidade do Hermes Agent sem perder conteúdo técnico. Ativa um modo de resposta ultra objetivo em PT-BR ou no idioma do usuário, preservando comandos, código, erros, nomes de APIs e avisos críticos. Inclui padrões para resposta curta, mensagens de commit, revisão de código e compressão segura de textos de memória/instruções. |
| [`database-postgres-prisma`](#database-postgres-prisma) | `curso-hermes/` | Use quando o aluno estiver modelando banco, criando migrations, usando PostgreSQL/MySQL/Prisma ou investigando lentidão/erro de query. Foca em schema simples, índices, transações, paginação e migração segura. |
| [`docker-deploy-basics`](#docker-deploy-basics) | `curso-hermes/` | Use quando o aluno quiser containerizar ou publicar uma aplicação. Cobre Dockerfile simples, Compose, variáveis de ambiente, healthcheck, logs, rollback básico e validação pós-deploy. |
| [`frontend-browser-qa`](#frontend-browser-qa) | `curso-hermes/` | Use quando o aluno precisar validar visualmente uma aplicação web. Define fluxo de QA com navegador: abrir app, testar caminho feliz, estados de erro/vazio, responsividade, console, network e acessibilidade básica. |
| [`frontend-react-nextjs`](#frontend-react-nextjs) | `curso-hermes/` | Use quando o aluno estiver criando ou revisando frontend React/Next.js. Cobre componentes, estado, forms, acessibilidade, performance, responsividade, UX e build sem transformar o projeto em arquitetura exagerada. |
| [`github-workflow-student`](#github-workflow-student) | `curso-hermes/` | Use quando o aluno trabalhar com GitHub: criar repo, commits, branches, pull requests, issues, releases e CI básico. Foca em fluxo seguro e simples para projetos de estudo e MVPs. |
| [`mcp-server-builder`](#mcp-server-builder) | `curso-hermes/` | Use quando o aluno quiser criar um MCP server para Hermes/agents. Orienta design de tools, schemas, validação, stdio/HTTP, segurança, testes locais e documentação mínima. |
| [`security-review-webapp`](#security-review-webapp) | `curso-hermes/` | Use quando o aluno criar autenticação, API, upload, pagamento, painel admin, integração externa ou qualquer código com dados sensíveis. Aplica checklist prático de segurança web antes de publicar. |
| [`testing-quality-gates`](#testing-quality-gates) | `curso-hermes/` | Use quando o aluno implementar feature/correção e precisar provar que funciona. Define gates de qualidade: teste mínimo, build, lint, E2E quando aplicável, regressão e evidência real de execução. |
| [`vibe-coding-starter`](#vibe-coding-starter) | `curso-hermes/` | Use quando o aluno quiser transformar uma ideia vaga em um sistema funcional com Hermes Agent. Define fluxo de vibe coding seguro: intenção, escopo, arquitetura mínima, fatias verticais, implementação, teste, revisão e validação real antes de declarar pronto. |
| [`agenda-ops`](#agenda-ops) | `forumtelecom/` | Use when the user asks Hermes to manage agenda, calendar, reminders, appointments, follow-ups, meeting schedules, service windows, recurring tasks, technician visits, or operational planning. Guides safe use of Google Calendar/Workspace, Hermes cron reminders, WhatsApp confirmations, and structured scheduling without exposing personal data. |
| [`blockbit-firewall-ops`](#blockbit-firewall-ops) | `forumtelecom/` | Senior Blockbit firewall/UTM engineer for ISP/MSP and enterprise operations. Use when the user asks to diagnose, audit, configure, or troubleshoot Blockbit firewalls: interfaces, routes, gateways, security policies, NAT, VPN IPsec/SSL, web filtering, application control, IPS/IDS, logs, HA, backups, updates, CLI/SSH checks, packet capture and Zabbix/SNMP monitoring. Triggers include Blockbit, firewall Blockbit, BB firewall, política Blockbit, NAT Blockbit, VPN Blockbit, IPsec Blockbit, UTM Blockbit, filtro web Blockbit, appliance Blockbit. |
| [`cisco-catalyst-switch-ops`](#cisco-catalyst-switch-ops) | `forumtelecom/` | Senior Cisco Catalyst switch engineer. Use when the user asks to diagnose, configure, audit, or troubleshoot Cisco switching on Catalyst IOS/IOS-XE: VLANs, trunks, access ports, STP/RSTP/MST, EtherChannel/LACP, PoE, DHCP snooping, port-security, 802.1X, interface errors, optics, and Zabbix/SNMP monitoring. |
| [`cisco-ops`](#cisco-ops) | `forumtelecom/` | Senior Cisco network engineer for IOS, IOS-XE, IOS-XR, and NX-OS edge/core routers. Use when the user asks to diagnose, configure, audit, or troubleshoot Cisco devices via SSH or NETCONF. Triggers include Cisco, IOS, IOS-XE, IOS-XR, NX-OS, ASR, ISR, Catalyst, Nexus, edge router, "show ip bgp", "show interfaces", "configure terminal", "wr mem", BGP Cisco, OSPF Cisco, MPLS, VRF, BGP route-reflector, ACL Cisco, "audit Cisco firewall", "Cisco edge router". |
| [`datacom-dmos-ops`](#datacom-dmos-ops) | `forumtelecom/` | Senior Datacom DmOS network engineer for Datacom switches, routers and access platforms running DmOS. Use when the user asks to diagnose, configure, audit, monitor, automate or troubleshoot Datacom/DMOS devices: DM4170, DM4050, DM4100/DM4100 ETH, DM4770, DmSwitch/DmOS, VLAN/dot1q, interface L2/L3, LAG/link aggregation, LLDP, BGP/OSPF, EAPS/ERPS, GPON, SNMP/Zabbix, transceivers, backup, commit and safe remote changes. Triggers include Datacom, DmOS, DMSwitch, DM4170, DM4050, DM4100, DM4770, show platform, show running-config, display json, commit, abort, copy mibs, dmos_vlan, datacom.dmos. |
| [`docker-ops`](#docker-ops) | `forumtelecom/` | Senior Docker engineer for container operations, Compose, networking, volumes, and troubleshooting. Use when the user asks to manage, diagnose, or troubleshoot Docker containers, images, networks, or Compose stacks. Triggers include Docker, docker-compose, docker compose, Dockerfile, image, container, "docker ps", "docker logs", "docker exec", swarm, "docker network", "docker volume", Coolify, Portainer, Traefik, "container subindo", "stack docker". |
| [`eve-ng-ops`](#eve-ng-ops) | `forumtelecom/` | Use when the user asks to install, operate, troubleshoot, back up, upgrade, or build network labs on EVE-NG/UNetLab: nested virtualization, Proxmox/VMware/bare metal deployment, web UI, labs, nodes, QEMU/IOL/Dynamips images, templates, fixpermissions, CPU/RAM/disk sizing, packet capture, bridges/cloud networks, performance, backups and safe handling of licensed vendor images. |
| [`financeiro-ops`](#financeiro-ops) | `forumtelecom/` | Use when the user asks Hermes to help with financeiro/administrative routines: contas a pagar/receber, cobranças, conciliação, fluxo de caixa, vencimentos, notas/boletos, planilhas financeiras, dashboards simples, lembretes de pagamento, and safe handling of financial data without exposing secrets or personal banking details. |
| [`fortigate-fortios`](#fortigate-fortios) | `forumtelecom/` | Senior Fortinet FortiGate/FortiOS firewall engineer. Use when the user asks to diagnose, configure, audit, or troubleshoot FortiGate/FortiOS 7.4/7.6: CLI, interfaces, routing, firewall policies, NAT, IPsec/SSL VPN, SD-WAN, UTM/security profiles, HA, FortiLink/FortiSwitch, FortiAnalyzer/syslog logging, FortiGuard, and diagnose debug flow/sniffer. |
| [`huawei-ne-ops`](#huawei-ne-ops) | `forumtelecom/` | Senior Huawei VRP network engineer for NE40, NE40E, NE8000, NE20, ME60 edge/core routers. Use when the user asks to diagnose, configure, audit, or troubleshoot Huawei VRP devices via SSH or NETCONF. Triggers include Huawei NE40, NE40E, NE8000, NE20, ME60, VRP, "display version", "display interface", "display bgp peer", "system-view", "commit", BGP Huawei, OSPF Huawei, MPLS Huawei, BNG Huawei, "Huawei edge router", "PE Huawei". |
| [`huawei-s67xx-switch-ops`](#huawei-s67xx-switch-ops) | `forumtelecom/` | Senior Huawei CloudEngine/CampusEngine S6730/S6720 switch engineer. Use when the user asks to diagnose, configure, audit, monitor, upgrade, or troubleshoot Huawei S6730, S6720, S6700/S67xx switches running VRP: VLAN, trunk/access/hybrid, Eth-Trunk/LACP, STP/RSTP/MSTP, stacking/iStack, MLAG/CSS where applicable, ACL, QoS, DHCP snooping, port-security, LLDP, SNMP/Zabbix, SFP/optical levels, port errors, firmware, backup/restore and safe remote changes. Triggers include Huawei S6730, Huawei S6720, CloudEngine S6730, S6720-HI, S6730-H, display interface brief, display device, display eth-trunk, display stp, display vlan, display stack, system-view, save. |
| [`hyper-v-ops`](#hyper-v-ops) | `forumtelecom/` | Senior Microsoft Hyper-V virtualization engineer for Windows Server and Windows client Hyper-V hosts. Use when the user asks to diagnose, configure, audit, or operate Hyper-V VMs, checkpoints, virtual switches, VLANs, NAT, VHD/VHDX storage, live migration, Replica, Failover Cluster, GPU-P/DDA, or PowerShell remoting. Triggers include Hyper-V, Get-VM, New-VM, Stop-VM, Restart-VM, Checkpoint-VM, VMSwitch, VHDX, Windows Server virtualization, Failover Cluster, Cluster Shared Volumes, Hyper-V Replica, PowerShell Direct, VMConnect, and Windows hypervisor. |
| [`mikrotik-ops`](#mikrotik-ops) | `forumtelecom/` | Senior MikroTik RouterOS network engineer. Use when the user asks to diagnose, configure, audit, or troubleshoot MikroTik devices via SSH or REST API. Triggers include MikroTik, RouterOS, Winbox, CCR, CRS, hAP, RB, BGP on MikroTik, hotspot MikroTik, PPPoE concentrator, CAPsMAN, queue tree, mangle, fasttrack, RouterOS 6 vs 7, /interface, /ip firewall, /routing, /system identity, .rsc export, "show me bgp peers", "block port on router", "list hotspot users", "audit firewall", "check failover". |
| [`mimosa-wireless-ops`](#mimosa-wireless-ops) | `forumtelecom/` | Use when the user asks to diagnose, configure, audit, align, monitor, or troubleshoot Mimosa wireless radios and antennas: C5c, C5x, C5, B5/B5c/B5-Lite, A5/A5c, point-to-point and point-to-multipoint ISP links, signal/SNR/MCS/noise/channel/GPS sync, bridge/VLAN, firmware, Mimosa Cloud, Web UI, SNMP and Zabbix checks. |
| [`olt-fiberhome-ops`](#olt-fiberhome-ops) | `forumtelecom/` | Senior FiberHome OLT engineer for AN5516, AN5116, AN6000 GPON/EPON platforms. Use when the user asks to provision, diagnose, or troubleshoot ONUs, PON ports, VLANs, or services on FiberHome OLTs. Triggers include FiberHome, AN5516, AN5116, AN6000, GEPON, GPON FiberHome, "autorizar ONU FiberHome", "desbloquear ONU", RP1000, RP1300, gponline, "olt fiberhome", "ONT FiberHome", "show pon status", "set whitelist". |
| [`olt-huawei-ops`](#olt-huawei-ops) | `forumtelecom/` | Senior Huawei OLT engineer for MA5800, MA5680T, MA5683T, MA5608T, MA5608, EA5800 GPON/EPON platforms. Use when the user asks to provision, diagnose, or troubleshoot ONTs, PON ports, VLANs, or services on Huawei OLTs. Triggers include MA5800, MA5680T, MA5683T, MA5608T, EA5800, MA5800-X7, MA5800-X15, MA5800-X17, "display ont info", "ont add", "service-port", "GPON Huawei", line-profile, ont-srvprofile, "olt huawei", "ONT Huawei", "auto-find ont", "autorizar ONT". |
| [`olt-intelbras-epon-ops`](#olt-intelbras-epon-ops) | `forumtelecom/` | Senior Intelbras EPON OLT engineer for OLT 4840 E/4840E and similar Intelbras EPON access networks. Use when the user asks to provision, diagnose, audit, monitor, back up or troubleshoot Intelbras EPON OLTs: ONU authorization, PON/EPON ports, VLAN/service profiles, uplinks, optical levels, MAC table, multicast/IPTV, SNMP/Zabbix, backup, firmware and safe changes. Triggers include Intelbras OLT 4840 E, OLT 4840E, OLT Intelbras EPON, ONU Intelbras offline, autorizar ONU Intelbras, EPON 4840, potência óptica, VLAN OLT Intelbras. |
| [`olt-vsol-ops`](#olt-vsol-ops) | `forumtelecom/` | Senior VSOL OLT engineer for GPON/EPON access networks. Use when the user asks to provision, diagnose, audit, or troubleshoot VSOL OLTs and compatible ONUs/ONTs: PON ports, ONU authorization, VLAN/service profiles, bridge/router modes, PPPoE/IPoE delivery, optical levels, uplinks, multicast/IPTV, CLI/Web/SNMP checks, backup and safe changes. Triggers include VSOL, V-SOL, V1600, V1600G, V1600D, V2800, GPON VSOL, EPON VSOL, OLT VSOL, autorizar ONU VSOL, ONT VSOL, ONU offline, potência óptica, optical power, DBA profile, line profile, service-port, VLAN OLT. |
| [`olt-zte-c300-ops`](#olt-zte-c300-ops) | `forumtelecom/` | Senior ZTE ZXA10 C300/C320 OLT engineer for GPON/EPON access networks. Use when the user asks to provision, diagnose, audit, or troubleshoot ZTE OLTs and ONUs/ONTs: C300, C320, ZXA10, GTGO, GTGH, ONU authorization, GPON ONU, VLAN/service-port, T-CONT/GEM, PPPoE/IPoE delivery, optical levels, uplinks, multicast/IPTV, CLI/Telnet/SSH/SNMP checks, backup and safe changes. Triggers include OLT ZTE, ZTE C300, ZTE C320, ZXA10 C300, ZXA10 C320, autorizar ONU ZTE, show onu unauthentication, gpon-onu, gpon-olt, pon-onu-mng, service-port, pon power attenuation. |
| [`opnsense-ops`](#opnsense-ops) | `forumtelecom/` | Senior OPNsense firewall engineer for ISP/MSP network operations. Use when the user asks to diagnose, audit, configure, or operate OPNsense firewalls via API, SSH/CLI, or web-GUI guidance: firewall rules, aliases, NAT, VLANs, interfaces, DHCP/Kea/dnsmasq, Unbound DNS, WireGuard/OpenVPN/IPsec status, HAProxy, gateways, routes, pf states/logs, config backup, firmware/plugins, and service health. Triggers include OPNsense, pfSense-like firewall, opn*, firewall rule, alias, NAT port forward, outbound NAT, VLAN OPNsense, Unbound, Kea DHCP, WireGuard OPNsense, HAProxy OPNsense, pfctl, configctl, filter reload, gateway status, CARP/HA. |
| [`proxmox-ops`](#proxmox-ops) | `forumtelecom/` | Senior Proxmox VE engineer for cluster management, VM/CT operations, storage, networking, and backup. Use when the user asks to create, diagnose, migrate, or troubleshoot KVM VMs (qm) or LXC containers (pct) on Proxmox VE. Triggers include Proxmox, PVE, Proxmox VE, qm, pct, pvesh, pvesm, pveceph, "proxmox cluster", "create vm proxmox", "lxc container", "proxmox backup", "vzdump", "ceph proxmox", "zfs proxmox". |
| [`sophos-firewall-ops`](#sophos-firewall-ops) | `forumtelecom/` | Senior Sophos Firewall/SFOS engineer for ISP/MSP and enterprise operations. Use when the user asks to diagnose, audit, configure, automate, monitor, or troubleshoot Sophos Firewall XG/XGS/SFOS: interfaces, zones, routing, firewall rules, NAT, IPsec/SSL VPN, web/application filtering, IPS, WAF, HA, logs, backups, firmware, API XML, CLI/SSH diagnostics, packet capture, SNMP and Zabbix monitoring. Triggers include Sophos Firewall, Sophos XG, Sophos XGS, SFOS, Sophos Central firewall, regra Sophos, NAT Sophos, VPN Sophos, IPsec Sophos, SSL VPN Sophos, web filter Sophos. |
| [`tr069-acs-ops`](#tr069-acs-ops) | `forumtelecom/` | Use when the user asks to design, install, operate, secure, monitor, or troubleshoot a TR-069/CWMP ACS environment for ISP networks: GenieACS, CPE/ONT/ONU/router onboarding, ACS URL, Inform, device parameters, presets/provisions, firmware/config push, WAN/PPPoE/Wi-Fi provisioning, API automation, Docker deployment, logs, security and Zabbix monitoring. |
| [`trendnet-switch-ops`](#trendnet-switch-ops) | `forumtelecom/` | Senior TRENDnet managed/Web Smart switch engineer. Use when the user asks to diagnose, configure, monitor, upgrade, or troubleshoot TRENDnet switches, especially TEG/TPE Web Smart, PoE, VLAN, SNMP, LLDP, LACP, STP/RSTP, port errors, firmware, backup/restore, and Zabbix monitoring. |
| [`ubiquiti-airmax-ops`](#ubiquiti-airmax-ops) | `forumtelecom/` | Use when the user asks to diagnose, configure, audit, align, monitor, or troubleshoot Ubiquiti airMAX radios and antennas: airMAX AC, airOS M/M5, NanoStation, NanoBeam, LiteBeam, PowerBeam, Rocket, Bullet, point-to-point and point-to-multipoint wireless links, signal/CCQ/noise/channel/frequency, bridge mode, VLAN, firmware, SSH/Web/UISP/SNMP checks. |
| [`vmware-ops`](#vmware-ops) | `forumtelecom/` | Senior VMware vSphere/vCenter/ESXi virtualization engineer for ISP/MSP and datacenter operations. Use when the user asks to diagnose, audit, configure, or operate VMware environments via vCenter REST API, VI/JSON, SOAP/pyVmomi, PowerCLI, ESXi SSH/esxcli, or web-GUI guidance: VMs, templates, snapshots, hosts, clusters, DRS/HA, datastores, vSAN, networks, port groups, distributed switches, vMotion, Storage vMotion, alarms, events, tasks, performance, VMware Tools, ISO/media, RBAC, permissions, lifecycle/vLCM, maintenance mode, and troubleshooting VM/host/storage/network issues. Triggers include VMware, vSphere, vCenter, ESXi, VMFS, datastore, snapshot, vMotion, DRS, HA, vSAN, PowerCLI, pyVmomi. |
| [`web-development-design-ops`](#web-development-design-ops) | `forumtelecom/` | Use when the user asks to create, improve, audit, or deploy high-quality custom websites, landing pages, institutional pages, dashboards, portals, or exclusive web interfaces with strong design, performance, SEO, accessibility, responsive layout, clean HTML/CSS/JS or modern frontend stacks, visual QA, Lighthouse-style validation and production-ready delivery. |
| [`zabbix-ops`](#zabbix-ops) | `forumtelecom/` | Senior Zabbix engineer for monitoring infrastructure (network devices, servers, containers) and creating templates programmatically while respecting API rate limits. Use when the user asks to query, configure, or troubleshoot Zabbix hosts, items, triggers, templates, problems, or maintenance windows; or to create/import templates in bulk respecting PHP-FPM and Postgres lock limits. Triggers include Zabbix, "zabbix api", "zabbix trigger", "zabbix template", "zabbix host", "zabbix problem", "zabbix maintenance", "zabbix snmp", "host está em problema", "criar template Zabbix", "criar template em massa", "import template Zabbix", "rate limit zabbix", "template.massadd", "configuration.import", Zabbix 6.x, Zabbix 7.x. |

## Curso Hermes / Alunos

### `backend-api-patterns`

**Arquivo:** [`.hermes/skills/curso-hermes/backend-api-patterns/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/backend-api-patterns/SKILL.md)

**O que faz:** Use quando o aluno estiver criando ou revisando backend/API. Cobre rotas REST, camada service/repository, validação, erros HTTP, autenticação, rate limit, paginação, logs e contrato entre frontend/backend.

**Tags:** `curso-hermes`, `backend`, `api`, `rest`, `node`, `fastapi`, `django`, `laravel`

**Quando usar:**

- Criar endpoint REST/GraphQL
- Organizar controller/service/repository
- Validar input
- Corrigir erro HTTP/API
- Integrar frontend com backend

**Como acionar no Hermes:**

```text
/skill backend-api-patterns
Desenhe esta API com rotas, validação e erros HTTP corretos.
```

**Validação típica:**

- Input validado por schema
- Erros não vazam stack/segredo
- Auth/permission checada no servidor
- Paginação em listas

---

### `caveman-terse-mode`

**Arquivo:** [`.hermes/skills/curso-hermes/caveman-terse-mode/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/caveman-terse-mode/SKILL.md)

**O que faz:** Use quando o aluno quiser reduzir tokens/verbosidade do Hermes Agent sem perder conteúdo técnico. Ativa um modo de resposta ultra objetivo em PT-BR ou no idioma do usuário, preservando comandos, código, erros, nomes de APIs e avisos críticos. Inclui padrões para resposta curta, mensagens de commit, revisão de código e compressão segura de textos de memória/instruções.

**Tags:** `hermes`, `curso-hermes`, `vibe-coding`, `token-economy`, `concise-output`, `code-review`, `commits`

**Quando usar:**

- "responda curto";
- "modo caveman";
- "economizar tokens";
- "seja direto";
- "sem enrolação";

**Como acionar no Hermes:**

```text
/skill caveman-terse-mode
Responda curto e gere commits/reviews objetivos.
```

**Validação típica:**

- Resposta preserva conteúdo técnico essencial
- Código/comandos/erros estão exatos
- Idioma do usuário foi mantido
- Riscos críticos não foram comprimidos demais

---

### `database-postgres-prisma`

**Arquivo:** [`.hermes/skills/curso-hermes/database-postgres-prisma/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/database-postgres-prisma/SKILL.md)

**O que faz:** Use quando o aluno estiver modelando banco, criando migrations, usando PostgreSQL/MySQL/Prisma ou investigando lentidão/erro de query. Foca em schema simples, índices, transações, paginação e migração segura.

**Tags:** `curso-hermes`, `database`, `postgres`, `mysql`, `prisma`, `migrations`

**Quando usar:**

- Criar schema/tabelas
- Escrever migration
- Corrigir query lenta
- Usar Prisma/ORM
- Definir relacionamento e índices

**Como acionar no Hermes:**

```text
/skill database-postgres-prisma
Me ajude com esta tarefa usando esta skill.
```

**Validação típica:**

- Campos obrigatórios realmente precisam ser obrigatórios
- Índices cobrem filtros principais
- Constraints protegem integridade
- Migration tem rollback/plano de recuperação

---

### `docker-deploy-basics`

**Arquivo:** [`.hermes/skills/curso-hermes/docker-deploy-basics/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/docker-deploy-basics/SKILL.md)

**O que faz:** Use quando o aluno quiser containerizar ou publicar uma aplicação. Cobre Dockerfile simples, Compose, variáveis de ambiente, healthcheck, logs, rollback básico e validação pós-deploy.

**Tags:** `curso-hermes`, `docker`, `compose`, `deploy`, `devops`

**Quando usar:**

- Criar Dockerfile
- Criar docker-compose
- Subir app com banco/cache
- Debugar container que não inicia
- Preparar deploy simples

**Como acionar no Hermes:**

```text
/skill docker-deploy-basics
Analise este docker-compose e corrija o serviço que não sobe.
```

**Validação típica:**

- Base image oficial e fixa por versão
- `WORKDIR` definido
- Dependências instaladas antes do copy completo para cache
- Build separado de runtime quando fizer sentido

---

### `frontend-browser-qa`

**Arquivo:** [`.hermes/skills/curso-hermes/frontend-browser-qa/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/frontend-browser-qa/SKILL.md)

**O que faz:** Use quando o aluno precisar validar visualmente uma aplicação web. Define fluxo de QA com navegador: abrir app, testar caminho feliz, estados de erro/vazio, responsividade, console, network e acessibilidade básica.

**Tags:** `curso-hermes`, `browser-qa`, `e2e`, `playwright`, `frontend`, `validation`

**Quando usar:**

- Depois de criar/alterar tela
- Antes de dizer "está funcionando"
- Para validar fluxo de login/cadastro/checkout/dashboard
- Quando o aluno diz "ficou bugado" ou manda print

**Como acionar no Hermes:**

```text
/skill frontend-browser-qa
Crie/revise esta tela React/Next.js e valide no navegador.
```

---

### `frontend-react-nextjs`

**Arquivo:** [`.hermes/skills/curso-hermes/frontend-react-nextjs/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/frontend-react-nextjs/SKILL.md)

**O que faz:** Use quando o aluno estiver criando ou revisando frontend React/Next.js. Cobre componentes, estado, forms, acessibilidade, performance, responsividade, UX e build sem transformar o projeto em arquitetura exagerada.

**Tags:** `curso-hermes`, `frontend`, `react`, `nextjs`, `ui`, `accessibility`

**Quando usar:**

- Criar tela, landing page, dashboard ou componente
- Corrigir build/erro de React/Next
- Melhorar responsividade/performance
- Revisar acessibilidade
- Organizar estado/forms

**Como acionar no Hermes:**

```text
/skill frontend-react-nextjs
Crie/revise esta tela React/Next.js e valide no navegador.
```

**Validação típica:**

- UI renderiza sem erro no console
- Fluxo principal funciona com mouse e teclado
- Mobile não quebra
- Build/lint/teste rodou ou bloqueio foi informado

---

### `github-workflow-student`

**Arquivo:** [`.hermes/skills/curso-hermes/github-workflow-student/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/github-workflow-student/SKILL.md)

**O que faz:** Use quando o aluno trabalhar com GitHub: criar repo, commits, branches, pull requests, issues, releases e CI básico. Foca em fluxo seguro e simples para projetos de estudo e MVPs.

**Tags:** `curso-hermes`, `github`, `git`, `pull-request`, `ci`

**Quando usar:**

- Criar/clonar repo
- Organizar branch
- Gerar commit message
- Abrir PR
- Revisar diff

**Como acionar no Hermes:**

```text
/skill github-workflow-student
Organize branch, commit e PR deste projeto.
```

---

### `mcp-server-builder`

**Arquivo:** [`.hermes/skills/curso-hermes/mcp-server-builder/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/mcp-server-builder/SKILL.md)

**O que faz:** Use quando o aluno quiser criar um MCP server para Hermes/agents. Orienta design de tools, schemas, validação, stdio/HTTP, segurança, testes locais e documentação mínima.

**Tags:** `curso-hermes`, `mcp`, `tools`, `integrations`, `hermes-agent`

**Quando usar:**

- Criar integração externa para Hermes
- Expor API interna como ferramenta
- Criar tool para banco, CRM, NOC, arquivos ou automação
- Ensinar aluno a conectar sistemas ao agente

**Como acionar no Hermes:**

```text
/skill mcp-server-builder
Crie um MCP server simples para esta integração.
```

**Validação típica:**

- Não expor segredo na resposta
- Não aceitar comando shell arbitrário
- Validar IDs/paths/URLs
- Rate limit/timeouts

---

### `security-review-webapp`

**Arquivo:** [`.hermes/skills/curso-hermes/security-review-webapp/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/security-review-webapp/SKILL.md)

**O que faz:** Use quando o aluno criar autenticação, API, upload, pagamento, painel admin, integração externa ou qualquer código com dados sensíveis. Aplica checklist prático de segurança web antes de publicar.

**Tags:** `curso-hermes`, `security`, `webapp`, `auth`, `secrets`, `owasp`

**Quando usar:**

- Login/autenticação/autorização
- API nova
- Upload de arquivo
- Dados pessoais/sensíveis
- Pagamento/webhook

**Como acionar no Hermes:**

```text
/skill security-review-webapp
Revise este projeto/API antes de publicar.
```

**Validação típica:**

- Nenhum token/senha hardcoded
- `.env` fora do git
- Logs não imprimem segredo
- Chaves de produção não usadas localmente sem necessidade

---

### `testing-quality-gates`

**Arquivo:** [`.hermes/skills/curso-hermes/testing-quality-gates/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/testing-quality-gates/SKILL.md)

**O que faz:** Use quando o aluno implementar feature/correção e precisar provar que funciona. Define gates de qualidade: teste mínimo, build, lint, E2E quando aplicável, regressão e evidência real de execução.

**Tags:** `curso-hermes`, `testing`, `tdd`, `quality`, `build`, `regression`

**Quando usar:**

- Depois de alterar código
- Ao corrigir bug
- Antes de entregar MVP
- Quando o aluno diz "acho que funcionou"

**Como acionar no Hermes:**

```text
/skill testing-quality-gates
Crie gates de teste/build/lint para esta mudança.
```

---

### `vibe-coding-starter`

**Arquivo:** [`.hermes/skills/curso-hermes/vibe-coding-starter/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/vibe-coding-starter/SKILL.md)

**O que faz:** Use quando o aluno quiser transformar uma ideia vaga em um sistema funcional com Hermes Agent. Define fluxo de vibe coding seguro: intenção, escopo, arquitetura mínima, fatias verticais, implementação, teste, revisão e validação real antes de declarar pronto.

**Tags:** `curso-hermes`, `vibe-coding`, `planning`, `mvp`, `software-development`

**Quando usar:**

- "Cria um SaaS/app/site/sistema pra mim"
- "Tenho uma ideia, me ajuda a fazer"
- "Faz um MVP"
- "Transforma esse briefing em projeto"
- Aluno está usando IA para programar sem método

**Como acionar no Hermes:**

```text
/skill vibe-coding-starter
Transforme esta ideia em um MVP com fatias e validação.
```

---

## Infraestrutura / Fórum Telecom

### `agenda-ops`

**Arquivo:** [`.hermes/skills/forumtelecom/agenda-ops/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/forumtelecom/agenda-ops/SKILL.md)

**O que faz:** Use when the user asks Hermes to manage agenda, calendar, reminders, appointments, follow-ups, meeting schedules, service windows, recurring tasks, technician visits, or operational planning. Guides safe use of Google Calendar/Workspace, Hermes cron reminders, WhatsApp confirmations, and structured scheduling without exposing personal data.

**Tags:** `agenda`, `calendar`, `reminders`, `cron`, `google-calendar`, `whatsapp`, `operations`

**Quando usar:**

- marcar reunião ou visita;
- criar lembrete único ou recorrente;
- consultar agenda do dia/semana;
- reagendar/cancelar compromisso;
- criar janela de manutenção com checklist;

**Como acionar no Hermes:**

```text
/skill agenda-ops
Me ajude com esta tarefa usando esta skill.
```

**Validação típica:**

- data/hora/fuso confirmados;
- duração definida;
- canal/local definido;
- participantes tratados com privacidade;

---

### `blockbit-firewall-ops`

**Arquivo:** [`.hermes/skills/forumtelecom/blockbit-firewall-ops/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/forumtelecom/blockbit-firewall-ops/SKILL.md)

**O que faz:** Senior Blockbit firewall/UTM engineer for ISP/MSP and enterprise operations. Use when the user asks to diagnose, audit, configure, or troubleshoot Blockbit firewalls: interfaces, routes, gateways, security policies, NAT, VPN IPsec/SSL, web filtering, application control, IPS/IDS, logs, HA, backups, updates, CLI/SSH checks, packet capture and Zabbix/SNMP monitoring. Triggers include Blockbit, firewall Blockbit, BB firewall, política Blockbit, NAT Blockbit, VPN Blockbit, IPsec Blockbit, UTM Blockbit, filtro web Blockbit, appliance Blockbit.

**Tags:** `blockbit`, `firewall`, `utm`, `vpn`, `nat`, `security`, `ips`, `webfilter`, `networking`

**Quando usar:**

- Senior Blockbit firewall/UTM engineer for ISP/MSP and enterprise operations. Use when the user asks to diagnose, audit, configure, or troubleshoot Blockbit firewalls: interfaces, routes, gateways, security policies, NAT, VPN IPsec/SSL, web filtering, application control, IPS/IDS, logs, HA, backups, updates, CLI/SSH checks, packet capture and Zabbix/SNMP monitoring. Triggers include Blockbit, firewall Blockbit, BB firewall, política Blockbit, NAT Blockbit, VPN Blockbit, IPsec Blockbit, UTM Blockbit, filtro web Blockbit, appliance Blockbit.

**Como acionar no Hermes:**

```text
/skill blockbit-firewall-ops
Me ajude com esta tarefa usando esta skill.
```

---

### `cisco-catalyst-switch-ops`

**Arquivo:** [`.hermes/skills/forumtelecom/cisco-catalyst-switch-ops/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/forumtelecom/cisco-catalyst-switch-ops/SKILL.md)

**O que faz:** Senior Cisco Catalyst switch engineer. Use when the user asks to diagnose, configure, audit, or troubleshoot Cisco switching on Catalyst IOS/IOS-XE: VLANs, trunks, access ports, STP/RSTP/MST, EtherChannel/LACP, PoE, DHCP snooping, port-security, 802.1X, interface errors, optics, and Zabbix/SNMP monitoring.

**Tags:** `cisco`, `catalyst`, `switch`, `ios`, `ios-xe`, `vlan`, `stp`, `lacp`, `poe`, `zabbix`, `forumtelecom`

**Quando usar:**

- Cisco Catalyst 2960, 3560, 3750, 3850, 9200, 9300, 9400, 9500, 9600.
- IOS/IOS-XE switching: VLAN, trunk, access port, SVI, inter-VLAN routing.
- STP/RSTP/PVST/MST root, blocked ports, topology changes, loops.
- EtherChannel/LACP/PAgP, port-channel blackhole, member mismatch.
- PoE/PoE+ issues with APs, câmeras, telefones IP.

**Como acionar no Hermes:**

```text
/skill cisco-catalyst-switch-ops
Me ajude com esta tarefa usando esta skill.
```

**Validação típica:**

- Model, IOS/IOS-XE version, stack state and management path were identified.
- Config/snapshot exists before any mutating action.
- Risky commands were explicitly confirmed.
- VLAN/trunk/STP/EtherChannel/PoE changes were validated with `show` commands.

---

### `cisco-ops`

**Arquivo:** [`.hermes/skills/forumtelecom/cisco-ops/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/forumtelecom/cisco-ops/SKILL.md)

**O que faz:** Senior Cisco network engineer for IOS, IOS-XE, IOS-XR, and NX-OS edge/core routers. Use when the user asks to diagnose, configure, audit, or troubleshoot Cisco devices via SSH or NETCONF. Triggers include Cisco, IOS, IOS-XE, IOS-XR, NX-OS, ASR, ISR, Catalyst, Nexus, edge router, "show ip bgp", "show interfaces", "configure terminal", "wr mem", BGP Cisco, OSPF Cisco, MPLS, VRF, BGP route-reflector, ACL Cisco, "audit Cisco firewall", "Cisco edge router".

**Quando usar:**

- Senior Cisco network engineer for IOS, IOS-XE, IOS-XR, and NX-OS edge/core routers. Use when the user asks to diagnose, configure, audit, or troubleshoot Cisco devices via SSH or NETCONF. Triggers include Cisco, IOS, IOS-XE, IOS-XR, NX-OS, ASR, ISR, Catalyst, Nexus, edge router, "show ip bgp", "show interfaces", "configure terminal", "wr mem", BGP Cisco, OSPF Cisco, MPLS, VRF, BGP route-reflector, ACL Cisco, "audit Cisco firewall", "Cisco edge router".

**Como acionar no Hermes:**

```text
/skill cisco-ops
Me ajude com esta tarefa usando esta skill.
```

---

### `datacom-dmos-ops`

**Arquivo:** [`.hermes/skills/forumtelecom/datacom-dmos-ops/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/forumtelecom/datacom-dmos-ops/SKILL.md)

**O que faz:** Senior Datacom DmOS network engineer for Datacom switches, routers and access platforms running DmOS. Use when the user asks to diagnose, configure, audit, monitor, automate or troubleshoot Datacom/DMOS devices: DM4170, DM4050, DM4100/DM4100 ETH, DM4770, DmSwitch/DmOS, VLAN/dot1q, interface L2/L3, LAG/link aggregation, LLDP, BGP/OSPF, EAPS/ERPS, GPON, SNMP/Zabbix, transceivers, backup, commit and safe remote changes. Triggers include Datacom, DmOS, DMSwitch, DM4170, DM4050, DM4100, DM4770, show platform, show running-config, display json, commit, abort, copy mibs, dmos_vlan, datacom.dmos.

**Tags:** `datacom`, `dmos`, `dmswitch`, `switch`, `router`, `olt`, `vlan`, `lag`, `lldp`, `gpon`, `bgp`, `ospf`, `zabbix`, `snmp`, `telecom`

**Quando usar:**

- Datacom DmOS, DmSwitch e plataformas DMxxxx que usem CLI DmOS;
- diagnóstico de portas, transceivers, VLAN/dot1q, L2/L3, LAG/link aggregation e LLDP;
- rotas, BGP/OSPF quando o DmOS estiver atuando em L3;
- EAPS/ERPS em redes metro;
- GPON/ONU em plataformas DmOS com módulos/recursos GPON;

**Como acionar no Hermes:**

```text
/skill datacom-dmos-ops
Me ajude com esta tarefa usando esta skill.
```

---

### `docker-ops`

**Arquivo:** [`.hermes/skills/forumtelecom/docker-ops/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/forumtelecom/docker-ops/SKILL.md)

**O que faz:** Senior Docker engineer for container operations, Compose, networking, volumes, and troubleshooting. Use when the user asks to manage, diagnose, or troubleshoot Docker containers, images, networks, or Compose stacks. Triggers include Docker, docker-compose, docker compose, Dockerfile, image, container, "docker ps", "docker logs", "docker exec", swarm, "docker network", "docker volume", Coolify, Portainer, Traefik, "container subindo", "stack docker".

**Quando usar:**

- Senior Docker engineer for container operations, Compose, networking, volumes, and troubleshooting. Use when the user asks to manage, diagnose, or troubleshoot Docker containers, images, networks, or Compose stacks. Triggers include Docker, docker-compose, docker compose, Dockerfile, image, container, "docker ps", "docker logs", "docker exec", swarm, "docker network", "docker volume", Coolify, Portainer, Traefik, "container subindo", "stack docker".

**Como acionar no Hermes:**

```text
/skill docker-ops
Analise este docker-compose e corrija o serviço que não sobe.
```

---

### `eve-ng-ops`

**Arquivo:** [`.hermes/skills/forumtelecom/eve-ng-ops/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/forumtelecom/eve-ng-ops/SKILL.md)

**O que faz:** Use when the user asks to install, operate, troubleshoot, back up, upgrade, or build network labs on EVE-NG/UNetLab: nested virtualization, Proxmox/VMware/bare metal deployment, web UI, labs, nodes, QEMU/IOL/Dynamips images, templates, fixpermissions, CPU/RAM/disk sizing, packet capture, bridges/cloud networks, performance, backups and safe handling of licensed vendor images.

**Tags:** `eve-ng`, `unetlab`, `network-emulator`, `qemu`, `iol`, `dynamips`, `labs`, `virtualization`, `telecom`

**Quando usar:**

- instalar EVE-NG Community/Professional;
- subir EVE-NG em Proxmox, VMware ESXi/Workstation ou bare metal;
- corrigir node que não inicia;
- adicionar imagem QEMU/IOL/Dynamips;
- rodar `fixpermissions`;

**Como acionar no Hermes:**

```text
/skill eve-ng-ops
Me ajude com esta tarefa usando esta skill.
```

**Validação típica:**

- EVE-NG identificado e acessível;
- CPU/RAM/disco/nested virtualization validados;
- serviços web/banco OK;
- labs e imagens com backup antes de mudança;

---

### `financeiro-ops`

**Arquivo:** [`.hermes/skills/forumtelecom/financeiro-ops/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/forumtelecom/financeiro-ops/SKILL.md)

**O que faz:** Use when the user asks Hermes to help with financeiro/administrative routines: contas a pagar/receber, cobranças, conciliação, fluxo de caixa, vencimentos, notas/boletos, planilhas financeiras, dashboards simples, lembretes de pagamento, and safe handling of financial data without exposing secrets or personal banking details.

**Tags:** `financeiro`, `contas-a-pagar`, `contas-a-receber`, `cobranca`, `fluxo-de-caixa`, `sheets`, `reports`

**Quando usar:**

- listar vencimentos do dia/semana;
- montar controle de contas a pagar/receber;
- gerar lembrete de cobrança;
- resumir inadimplência por cliente/período;
- criar planilha de fluxo de caixa;

**Como acionar no Hermes:**

```text
/skill financeiro-ops
Me ajude com esta tarefa usando esta skill.
```

**Validação típica:**

- fonte de dados identificada;
- dados sensíveis mascarados;
- datas e valores normalizados;
- totais conferidos;

---

### `fortigate-fortios`

**Arquivo:** [`.hermes/skills/forumtelecom/fortigate-fortios/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/forumtelecom/fortigate-fortios/SKILL.md)

**O que faz:** Senior Fortinet FortiGate/FortiOS firewall engineer. Use when the user asks to diagnose, configure, audit, or troubleshoot FortiGate/FortiOS 7.4/7.6: CLI, interfaces, routing, firewall policies, NAT, IPsec/SSL VPN, SD-WAN, UTM/security profiles, HA, FortiLink/FortiSwitch, FortiAnalyzer/syslog logging, FortiGuard, and diagnose debug flow/sniffer.

**Tags:** `fortigate`, `fortios`, `fortinet`, `firewall`, `vpn`, `sd-wan`, `ha`, `utm`

**Quando usar:**

- Senior Fortinet FortiGate/FortiOS firewall engineer. Use when the user asks to diagnose, configure, audit, or troubleshoot FortiGate/FortiOS 7.4/7.6: CLI, interfaces, routing, firewall policies, NAT, IPsec/SSL VPN, SD-WAN, UTM/security profiles, HA, FortiLink/FortiSwitch, FortiAnalyzer/syslog logging, FortiGuard, and diagnose debug flow/sniffer.

**Como acionar no Hermes:**

```text
/skill fortigate-fortios
Me ajude com esta tarefa usando esta skill.
```

---

### `huawei-ne-ops`

**Arquivo:** [`.hermes/skills/forumtelecom/huawei-ne-ops/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/forumtelecom/huawei-ne-ops/SKILL.md)

**O que faz:** Senior Huawei VRP network engineer for NE40, NE40E, NE8000, NE20, ME60 edge/core routers. Use when the user asks to diagnose, configure, audit, or troubleshoot Huawei VRP devices via SSH or NETCONF. Triggers include Huawei NE40, NE40E, NE8000, NE20, ME60, VRP, "display version", "display interface", "display bgp peer", "system-view", "commit", BGP Huawei, OSPF Huawei, MPLS Huawei, BNG Huawei, "Huawei edge router", "PE Huawei".

**Quando usar:**

- Senior Huawei VRP network engineer for NE40, NE40E, NE8000, NE20, ME60 edge/core routers. Use when the user asks to diagnose, configure, audit, or troubleshoot Huawei VRP devices via SSH or NETCONF. Triggers include Huawei NE40, NE40E, NE8000, NE20, ME60, VRP, "display version", "display interface", "display bgp peer", "system-view", "commit", BGP Huawei, OSPF Huawei, MPLS Huawei, BNG Huawei, "Huawei edge router", "PE Huawei".

**Como acionar no Hermes:**

```text
/skill huawei-ne-ops
Me ajude com esta tarefa usando esta skill.
```

---

### `huawei-s67xx-switch-ops`

**Arquivo:** [`.hermes/skills/forumtelecom/huawei-s67xx-switch-ops/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/forumtelecom/huawei-s67xx-switch-ops/SKILL.md)

**O que faz:** Senior Huawei CloudEngine/CampusEngine S6730/S6720 switch engineer. Use when the user asks to diagnose, configure, audit, monitor, upgrade, or troubleshoot Huawei S6730, S6720, S6700/S67xx switches running VRP: VLAN, trunk/access/hybrid, Eth-Trunk/LACP, STP/RSTP/MSTP, stacking/iStack, MLAG/CSS where applicable, ACL, QoS, DHCP snooping, port-security, LLDP, SNMP/Zabbix, SFP/optical levels, port errors, firmware, backup/restore and safe remote changes. Triggers include Huawei S6730, Huawei S6720, CloudEngine S6730, S6720-HI, S6730-H, display interface brief, display device, display eth-trunk, display stp, display vlan, display stack, system-view, save.

**Tags:** `huawei`, `s6730`, `s6720`, `s67xx`, `switch`, `vrp`, `vlan`, `eth-trunk`, `stp`, `istack`, `snmp`, `zabbix`, `telecom`

**Quando usar:**

- Huawei S6730, S6720, S6720-HI, S6730-H, S6730S, S6700/S67xx;
- VLAN, trunk, access, hybrid e QinQ básico;
- Eth-Trunk/LACP, uplink, agregação e balanceamento;
- STP/RSTP/MSTP, loop, bloqueio de porta e root bridge;
- stack/iStack, membro com problema, split-brain e renumeração;

**Como acionar no Hermes:**

```text
/skill huawei-s67xx-switch-ops
Me ajude com esta tarefa usando esta skill.
```

**Validação típica:**

- modelo/versão/stack identificados;
- snapshot de configuração e interfaces coletado;
- caminho de gerência/rollback confirmado;
- VLAN/trunk/Eth-Trunk/STP atual entendido antes da mudança;

---

### `hyper-v-ops`

**Arquivo:** [`.hermes/skills/forumtelecom/hyper-v-ops/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/forumtelecom/hyper-v-ops/SKILL.md)

**O que faz:** Senior Microsoft Hyper-V virtualization engineer for Windows Server and Windows client Hyper-V hosts. Use when the user asks to diagnose, configure, audit, or operate Hyper-V VMs, checkpoints, virtual switches, VLANs, NAT, VHD/VHDX storage, live migration, Replica, Failover Cluster, GPU-P/DDA, or PowerShell remoting. Triggers include Hyper-V, Get-VM, New-VM, Stop-VM, Restart-VM, Checkpoint-VM, VMSwitch, VHDX, Windows Server virtualization, Failover Cluster, Cluster Shared Volumes, Hyper-V Replica, PowerShell Direct, VMConnect, and Windows hypervisor.

**Tags:** `hyper-v`, `windows-server`, `virtualization`, `powershell`, `infrastructure`

**Quando usar:**

- Senior Microsoft Hyper-V virtualization engineer for Windows Server and Windows client Hyper-V hosts. Use when the user asks to diagnose, configure, audit, or operate Hyper-V VMs, checkpoints, virtual switches, VLANs, NAT, VHD/VHDX storage, live migration, Replica, Failover Cluster, GPU-P/DDA, or PowerShell remoting. Triggers include Hyper-V, Get-VM, New-VM, Stop-VM, Restart-VM, Checkpoint-VM, VMSwitch, VHDX, Windows Server virtualization, Failover Cluster, Cluster Shared Volumes, Hyper-V Replica, PowerShell Direct, VMConnect, and Windows hypervisor.

**Como acionar no Hermes:**

```text
/skill hyper-v-ops
Me ajude com esta tarefa usando esta skill.
```

---

### `mikrotik-ops`

**Arquivo:** [`.hermes/skills/forumtelecom/mikrotik-ops/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/forumtelecom/mikrotik-ops/SKILL.md)

**O que faz:** Senior MikroTik RouterOS network engineer. Use when the user asks to diagnose, configure, audit, or troubleshoot MikroTik devices via SSH or REST API. Triggers include MikroTik, RouterOS, Winbox, CCR, CRS, hAP, RB, BGP on MikroTik, hotspot MikroTik, PPPoE concentrator, CAPsMAN, queue tree, mangle, fasttrack, RouterOS 6 vs 7, /interface, /ip firewall, /routing, /system identity, .rsc export, "show me bgp peers", "block port on router", "list hotspot users", "audit firewall", "check failover".

**Quando usar:**

- Senior MikroTik RouterOS network engineer. Use when the user asks to diagnose, configure, audit, or troubleshoot MikroTik devices via SSH or REST API. Triggers include MikroTik, RouterOS, Winbox, CCR, CRS, hAP, RB, BGP on MikroTik, hotspot MikroTik, PPPoE concentrator, CAPsMAN, queue tree, mangle, fasttrack, RouterOS 6 vs 7, /interface, /ip firewall, /routing, /system identity, .rsc export, "show me bgp peers", "block port on router", "list hotspot users", "audit firewall", "check failover".

**Como acionar no Hermes:**

```text
/skill mikrotik-ops
Analise este RouterOS e proponha correção segura.
```

---

### `mimosa-wireless-ops`

**Arquivo:** [`.hermes/skills/forumtelecom/mimosa-wireless-ops/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/forumtelecom/mimosa-wireless-ops/SKILL.md)

**O que faz:** Use when the user asks to diagnose, configure, audit, align, monitor, or troubleshoot Mimosa wireless radios and antennas: C5c, C5x, C5, B5/B5c/B5-Lite, A5/A5c, point-to-point and point-to-multipoint ISP links, signal/SNR/MCS/noise/channel/GPS sync, bridge/VLAN, firmware, Mimosa Cloud, Web UI, SNMP and Zabbix checks.

**Tags:** `mimosa`, `c5c`, `c5x`, `b5`, `a5`, `wireless`, `ptmp`, `ptp`, `isp`, `snmp`, `zabbix`

**Quando usar:**

- C5c com sinal ruim, throughput baixo ou desconexões;
- cliente C5/C5c/C5x não registra no AP A5/A5c;
- enlace PTP B5/B5c instável;
- ajuste de frequência, largura de canal, potência ou antena;
- bridge/VLAN sem tráfego;

**Como acionar no Hermes:**

```text
/skill mimosa-wireless-ops
Me ajude com esta tarefa usando esta skill.
```

**Validação típica:**

- modelo/firmware/papel identificados;
- backup feito antes de mudança;
- RSSI/SNR/MCS/noise/canal/largura coletados;
- bridge/VLAN/LAN validadas se o problema é tráfego;

---

### `olt-fiberhome-ops`

**Arquivo:** [`.hermes/skills/forumtelecom/olt-fiberhome-ops/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/forumtelecom/olt-fiberhome-ops/SKILL.md)

**O que faz:** Senior FiberHome OLT engineer for AN5516, AN5116, AN6000 GPON/EPON platforms. Use when the user asks to provision, diagnose, or troubleshoot ONUs, PON ports, VLANs, or services on FiberHome OLTs. Triggers include FiberHome, AN5516, AN5116, AN6000, GEPON, GPON FiberHome, "autorizar ONU FiberHome", "desbloquear ONU", RP1000, RP1300, gponline, "olt fiberhome", "ONT FiberHome", "show pon status", "set whitelist".

**Quando usar:**

- Senior FiberHome OLT engineer for AN5516, AN5116, AN6000 GPON/EPON platforms. Use when the user asks to provision, diagnose, or troubleshoot ONUs, PON ports, VLANs, or services on FiberHome OLTs. Triggers include FiberHome, AN5516, AN5116, AN6000, GEPON, GPON FiberHome, "autorizar ONU FiberHome", "desbloquear ONU", RP1000, RP1300, gponline, "olt fiberhome", "ONT FiberHome", "show pon status", "set whitelist".

**Como acionar no Hermes:**

```text
/skill olt-fiberhome-ops
Diagnostique este problema de ONU/pon sem alterar configuração.
```

---

### `olt-huawei-ops`

**Arquivo:** [`.hermes/skills/forumtelecom/olt-huawei-ops/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/forumtelecom/olt-huawei-ops/SKILL.md)

**O que faz:** Senior Huawei OLT engineer for MA5800, MA5680T, MA5683T, MA5608T, MA5608, EA5800 GPON/EPON platforms. Use when the user asks to provision, diagnose, or troubleshoot ONTs, PON ports, VLANs, or services on Huawei OLTs. Triggers include MA5800, MA5680T, MA5683T, MA5608T, EA5800, MA5800-X7, MA5800-X15, MA5800-X17, "display ont info", "ont add", "service-port", "GPON Huawei", line-profile, ont-srvprofile, "olt huawei", "ONT Huawei", "auto-find ont", "autorizar ONT".

**Quando usar:**

- Senior Huawei OLT engineer for MA5800, MA5680T, MA5683T, MA5608T, MA5608, EA5800 GPON/EPON platforms. Use when the user asks to provision, diagnose, or troubleshoot ONTs, PON ports, VLANs, or services on Huawei OLTs. Triggers include MA5800, MA5680T, MA5683T, MA5608T, EA5800, MA5800-X7, MA5800-X15, MA5800-X17, "display ont info", "ont add", "service-port", "GPON Huawei", line-profile, ont-srvprofile, "olt huawei", "ONT Huawei", "auto-find ont", "autorizar ONT".

**Como acionar no Hermes:**

```text
/skill olt-huawei-ops
Diagnostique este problema de ONU/pon sem alterar configuração.
```

---

### `olt-intelbras-epon-ops`

**Arquivo:** [`.hermes/skills/forumtelecom/olt-intelbras-epon-ops/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/forumtelecom/olt-intelbras-epon-ops/SKILL.md)

**O que faz:** Senior Intelbras EPON OLT engineer for OLT 4840 E/4840E and similar Intelbras EPON access networks. Use when the user asks to provision, diagnose, audit, monitor, back up or troubleshoot Intelbras EPON OLTs: ONU authorization, PON/EPON ports, VLAN/service profiles, uplinks, optical levels, MAC table, multicast/IPTV, SNMP/Zabbix, backup, firmware and safe changes. Triggers include Intelbras OLT 4840 E, OLT 4840E, OLT Intelbras EPON, ONU Intelbras offline, autorizar ONU Intelbras, EPON 4840, potência óptica, VLAN OLT Intelbras.

**Tags:** `intelbras`, `olt`, `epon`, `ftth`, `onu`, `ont`, `vlan`, `snmp`, `zabbix`, `telecom`

**Quando usar:**

- Senior Intelbras EPON OLT engineer for OLT 4840 E/4840E and similar Intelbras EPON access networks. Use when the user asks to provision, diagnose, audit, monitor, back up or troubleshoot Intelbras EPON OLTs: ONU authorization, PON/EPON ports, VLAN/service profiles, uplinks, optical levels, MAC table, multicast/IPTV, SNMP/Zabbix, backup, firmware and safe changes. Triggers include Intelbras OLT 4840 E, OLT 4840E, OLT Intelbras EPON, ONU Intelbras offline, autorizar ONU Intelbras, EPON 4840, potência óptica, VLAN OLT Intelbras.

**Como acionar no Hermes:**

```text
/skill olt-intelbras-epon-ops
Diagnostique este problema de ONU/pon sem alterar configuração.
```

---

### `olt-vsol-ops`

**Arquivo:** [`.hermes/skills/forumtelecom/olt-vsol-ops/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/forumtelecom/olt-vsol-ops/SKILL.md)

**O que faz:** Senior VSOL OLT engineer for GPON/EPON access networks. Use when the user asks to provision, diagnose, audit, or troubleshoot VSOL OLTs and compatible ONUs/ONTs: PON ports, ONU authorization, VLAN/service profiles, bridge/router modes, PPPoE/IPoE delivery, optical levels, uplinks, multicast/IPTV, CLI/Web/SNMP checks, backup and safe changes. Triggers include VSOL, V-SOL, V1600, V1600G, V1600D, V2800, GPON VSOL, EPON VSOL, OLT VSOL, autorizar ONU VSOL, ONT VSOL, ONU offline, potência óptica, optical power, DBA profile, line profile, service-port, VLAN OLT.

**Tags:** `vsol`, `olt`, `gpon`, `epon`, `ftth`, `onu`, `ont`, `vlan`, `snmp`, `telecom`

**Quando usar:**

- Senior VSOL OLT engineer for GPON/EPON access networks. Use when the user asks to provision, diagnose, audit, or troubleshoot VSOL OLTs and compatible ONUs/ONTs: PON ports, ONU authorization, VLAN/service profiles, bridge/router modes, PPPoE/IPoE delivery, optical levels, uplinks, multicast/IPTV, CLI/Web/SNMP checks, backup and safe changes. Triggers include VSOL, V-SOL, V1600, V1600G, V1600D, V2800, GPON VSOL, EPON VSOL, OLT VSOL, autorizar ONU VSOL, ONT VSOL, ONU offline, potência óptica, optical power, DBA profile, line profile, service-port, VLAN OLT.

**Como acionar no Hermes:**

```text
/skill olt-vsol-ops
Diagnostique este problema de ONU/pon sem alterar configuração.
```

---

### `olt-zte-c300-ops`

**Arquivo:** [`.hermes/skills/forumtelecom/olt-zte-c300-ops/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/forumtelecom/olt-zte-c300-ops/SKILL.md)

**O que faz:** Senior ZTE ZXA10 C300/C320 OLT engineer for GPON/EPON access networks. Use when the user asks to provision, diagnose, audit, or troubleshoot ZTE OLTs and ONUs/ONTs: C300, C320, ZXA10, GTGO, GTGH, ONU authorization, GPON ONU, VLAN/service-port, T-CONT/GEM, PPPoE/IPoE delivery, optical levels, uplinks, multicast/IPTV, CLI/Telnet/SSH/SNMP checks, backup and safe changes. Triggers include OLT ZTE, ZTE C300, ZTE C320, ZXA10 C300, ZXA10 C320, autorizar ONU ZTE, show onu unauthentication, gpon-onu, gpon-olt, pon-onu-mng, service-port, pon power attenuation.

**Tags:** `zte`, `zxa10`, `c300`, `c320`, `olt`, `gpon`, `epon`, `ftth`, `onu`, `ont`, `vlan`, `snmp`, `telecom`

**Quando usar:**

- autorizar ONU/ONT em ZTE C300/C320;
- diagnosticar ONU offline, LOS, dying-gasp, sinal óptico ruim ou flapping;
- revisar VLAN, service-port, T-CONT, GEM port e porta UNI;
- validar uplink/trunk e entrega PPPoE/IPoE/IPTV;
- fazer backup, auditoria e leitura operacional da OLT;

**Como acionar no Hermes:**

```text
/skill olt-zte-c300-ops
Diagnostique este problema de ONU/pon sem alterar configuração.
```

**Validação típica:**

- modelo/versão/placas identificados;
- F/S/P e ONU_ID confirmados;
- backup/snapshot coletado antes da mudança;
- serial e `type` conferidos;

---

### `opnsense-ops`

**Arquivo:** [`.hermes/skills/forumtelecom/opnsense-ops/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/forumtelecom/opnsense-ops/SKILL.md)

**O que faz:** Senior OPNsense firewall engineer for ISP/MSP network operations. Use when the user asks to diagnose, audit, configure, or operate OPNsense firewalls via API, SSH/CLI, or web-GUI guidance: firewall rules, aliases, NAT, VLANs, interfaces, DHCP/Kea/dnsmasq, Unbound DNS, WireGuard/OpenVPN/IPsec status, HAProxy, gateways, routes, pf states/logs, config backup, firmware/plugins, and service health. Triggers include OPNsense, pfSense-like firewall, opn*, firewall rule, alias, NAT port forward, outbound NAT, VLAN OPNsense, Unbound, Kea DHCP, WireGuard OPNsense, HAProxy OPNsense, pfctl, configctl, filter reload, gateway status, CARP/HA.

**Tags:** `opnsense`, `firewall`, `networking`, `api`, `vpn`, `nat`, `dns`, `dhcp`

**Quando usar:**

- Senior OPNsense firewall engineer for ISP/MSP network operations. Use when the user asks to diagnose, audit, configure, or operate OPNsense firewalls via API, SSH/CLI, or web-GUI guidance: firewall rules, aliases, NAT, VLANs, interfaces, DHCP/Kea/dnsmasq, Unbound DNS, WireGuard/OpenVPN/IPsec status, HAProxy, gateways, routes, pf states/logs, config backup, firmware/plugins, and service health. Triggers include OPNsense, pfSense-like firewall, opn*, firewall rule, alias, NAT port forward, outbound NAT, VLAN OPNsense, Unbound, Kea DHCP, WireGuard OPNsense, HAProxy OPNsense, pfctl, configctl, filter reload, gateway status, CARP/HA.

**Como acionar no Hermes:**

```text
/skill opnsense-ops
Me ajude com esta tarefa usando esta skill.
```

---

### `proxmox-ops`

**Arquivo:** [`.hermes/skills/forumtelecom/proxmox-ops/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/forumtelecom/proxmox-ops/SKILL.md)

**O que faz:** Senior Proxmox VE engineer for cluster management, VM/CT operations, storage, networking, and backup. Use when the user asks to create, diagnose, migrate, or troubleshoot KVM VMs (qm) or LXC containers (pct) on Proxmox VE. Triggers include Proxmox, PVE, Proxmox VE, qm, pct, pvesh, pvesm, pveceph, "proxmox cluster", "create vm proxmox", "lxc container", "proxmox backup", "vzdump", "ceph proxmox", "zfs proxmox".

**Quando usar:**

- Senior Proxmox VE engineer for cluster management, VM/CT operations, storage, networking, and backup. Use when the user asks to create, diagnose, migrate, or troubleshoot KVM VMs (qm) or LXC containers (pct) on Proxmox VE. Triggers include Proxmox, PVE, Proxmox VE, qm, pct, pvesh, pvesm, pveceph, "proxmox cluster", "create vm proxmox", "lxc container", "proxmox backup", "vzdump", "ceph proxmox", "zfs proxmox".

**Como acionar no Hermes:**

```text
/skill proxmox-ops
Verifique este cluster/VM/storage e indique correção segura.
```

---

### `sophos-firewall-ops`

**Arquivo:** [`.hermes/skills/forumtelecom/sophos-firewall-ops/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/forumtelecom/sophos-firewall-ops/SKILL.md)

**O que faz:** Senior Sophos Firewall/SFOS engineer for ISP/MSP and enterprise operations. Use when the user asks to diagnose, audit, configure, automate, monitor, or troubleshoot Sophos Firewall XG/XGS/SFOS: interfaces, zones, routing, firewall rules, NAT, IPsec/SSL VPN, web/application filtering, IPS, WAF, HA, logs, backups, firmware, API XML, CLI/SSH diagnostics, packet capture, SNMP and Zabbix monitoring. Triggers include Sophos Firewall, Sophos XG, Sophos XGS, SFOS, Sophos Central firewall, regra Sophos, NAT Sophos, VPN Sophos, IPsec Sophos, SSL VPN Sophos, web filter Sophos.

**Tags:** `sophos`, `sfos`, `firewall`, `xg`, `xgs`, `vpn`, `nat`, `ips`, `webfilter`, `ha`, `api`

**Quando usar:**

- Senior Sophos Firewall/SFOS engineer for ISP/MSP and enterprise operations. Use when the user asks to diagnose, audit, configure, automate, monitor, or troubleshoot Sophos Firewall XG/XGS/SFOS: interfaces, zones, routing, firewall rules, NAT, IPsec/SSL VPN, web/application filtering, IPS, WAF, HA, logs, backups, firmware, API XML, CLI/SSH diagnostics, packet capture, SNMP and Zabbix monitoring. Triggers include Sophos Firewall, Sophos XG, Sophos XGS, SFOS, Sophos Central firewall, regra Sophos, NAT Sophos, VPN Sophos, IPsec Sophos, SSL VPN Sophos, web filter Sophos.

**Como acionar no Hermes:**

```text
/skill sophos-firewall-ops
Me ajude com esta tarefa usando esta skill.
```

**Validação típica:**

- Versão/modelo/SFOS confirmados.
- Escopo e risco da mudança entendidos.
- Backup/snapshot feito antes de alteração relevante.
- Segredos não foram expostos em chat, arquivo ou commit.

---

### `tr069-acs-ops`

**Arquivo:** [`.hermes/skills/forumtelecom/tr069-acs-ops/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/forumtelecom/tr069-acs-ops/SKILL.md)

**O que faz:** Use when the user asks to design, install, operate, secure, monitor, or troubleshoot a TR-069/CWMP ACS environment for ISP networks: GenieACS, CPE/ONT/ONU/router onboarding, ACS URL, Inform, device parameters, presets/provisions, firmware/config push, WAN/PPPoE/Wi-Fi provisioning, API automation, Docker deployment, logs, security and Zabbix monitoring.

**Tags:** `tr069`, `tr-069`, `cwmp`, `acs`, `genieacs`, `cpe`, `ont`, `onu`, `provisioning`, `isp`, `zabbix`

**Quando usar:**

- subir um ACS TR-069 do zero;
- instalar GenieACS com Docker ou Linux;
- configurar ACS URL em ONT/roteador;
- diagnosticar CPE que não aparece no ACS;
- criar presets/provisions;

**Como acionar no Hermes:**

```text
/skill tr069-acs-ops
Me ajude com esta tarefa usando esta skill.
```

**Validação típica:**

- ACS instalado e portas necessárias ouvindo;
- UI/API protegida por ACL/VPN/auth;
- MongoDB persistente e com backup;
- CPE de teste apareceu no ACS;

---

### `trendnet-switch-ops`

**Arquivo:** [`.hermes/skills/forumtelecom/trendnet-switch-ops/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/forumtelecom/trendnet-switch-ops/SKILL.md)

**O que faz:** Senior TRENDnet managed/Web Smart switch engineer. Use when the user asks to diagnose, configure, monitor, upgrade, or troubleshoot TRENDnet switches, especially TEG/TPE Web Smart, PoE, VLAN, SNMP, LLDP, LACP, STP/RSTP, port errors, firmware, backup/restore, and Zabbix monitoring.

**Tags:** `trendnet`, `switch`, `poe`, `vlan`, `snmp`, `zabbix`, `firmware`, `forumtelecom`

**Quando usar:**

- TRENDnet switch, TEG, TPE, TI industrial switches, Web Smart, EdgeSmart, L2 Managed.
- VLAN, trunk/access/hybrid, voice/private VLAN, 802.1Q issues.
- PoE/PoE+ budget, camera/AP reboot, port power, classification.
- SNMP v1/v2c/v3, MIB, Zabbix discovery, interface counters.
- Firmware upgrade, backup/restore, config export/import.

**Como acionar no Hermes:**

```text
/skill trendnet-switch-ops
Me ajude com esta tarefa usando esta skill.
```

**Validação típica:**

- Exact model, hardware revision, and firmware were identified.
- Official TRENDnet support page/manual/MIB/firmware matched the same revision.
- Backup/snapshot exists before any change.
- Management reachability was validated after changes.

---

### `ubiquiti-airmax-ops`

**Arquivo:** [`.hermes/skills/forumtelecom/ubiquiti-airmax-ops/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/forumtelecom/ubiquiti-airmax-ops/SKILL.md)

**O que faz:** Use when the user asks to diagnose, configure, audit, align, monitor, or troubleshoot Ubiquiti airMAX radios and antennas: airMAX AC, airOS M/M5, NanoStation, NanoBeam, LiteBeam, PowerBeam, Rocket, Bullet, point-to-point and point-to-multipoint wireless links, signal/CCQ/noise/channel/frequency, bridge mode, VLAN, firmware, SSH/Web/UISP/SNMP checks.

**Tags:** `ubiquiti`, `airmax`, `airos`, `m5`, `ac`, `wireless`, `ptp`, `ptmp`, `isp`, `snmp`

**Quando usar:**

- enlace PTP/PTMP instável;
- sinal ruim ou CCQ baixo;
- cliente desconectando em Rocket/AP;
- ajuste de frequência/canal/largura/potência;
- VLAN/bridge sem passar tráfego;

**Como acionar no Hermes:**

```text
/skill ubiquiti-airmax-ops
Me ajude com esta tarefa usando esta skill.
```

**Validação típica:**

- modelo/firmware identificados;
- backup feito antes de alteração;
- sinal, SNR, ruído, CCQ/quality e rates coletados;
- bridge/VLAN/LAN validadas quando o problema é tráfego;

---

### `vmware-ops`

**Arquivo:** [`.hermes/skills/forumtelecom/vmware-ops/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/forumtelecom/vmware-ops/SKILL.md)

**O que faz:** Senior VMware vSphere/vCenter/ESXi virtualization engineer for ISP/MSP and datacenter operations. Use when the user asks to diagnose, audit, configure, or operate VMware environments via vCenter REST API, VI/JSON, SOAP/pyVmomi, PowerCLI, ESXi SSH/esxcli, or web-GUI guidance: VMs, templates, snapshots, hosts, clusters, DRS/HA, datastores, vSAN, networks, port groups, distributed switches, vMotion, Storage vMotion, alarms, events, tasks, performance, VMware Tools, ISO/media, RBAC, permissions, lifecycle/vLCM, maintenance mode, and troubleshooting VM/host/storage/network issues. Triggers include VMware, vSphere, vCenter, ESXi, VMFS, datastore, snapshot, vMotion, DRS, HA, vSAN, PowerCLI, pyVmomi.

**Tags:** `vmware`, `vsphere`, `vcenter`, `esxi`, `virtualization`, `datacenter`, `powercli`, `pyvmomi`

**Quando usar:**

- Senior VMware vSphere/vCenter/ESXi virtualization engineer for ISP/MSP and datacenter operations. Use when the user asks to diagnose, audit, configure, or operate VMware environments via vCenter REST API, VI/JSON, SOAP/pyVmomi, PowerCLI, ESXi SSH/esxcli, or web-GUI guidance: VMs, templates, snapshots, hosts, clusters, DRS/HA, datastores, vSAN, networks, port groups, distributed switches, vMotion, Storage vMotion, alarms, events, tasks, performance, VMware Tools, ISO/media, RBAC, permissions, lifecycle/vLCM, maintenance mode, and troubleshooting VM/host/storage/network issues. Triggers include VMware, vSphere, vCenter, ESXi, VMFS, datastore, snapshot, vMotion, DRS, HA, vSAN, PowerCLI, pyVmomi.

**Como acionar no Hermes:**

```text
/skill vmware-ops
Me ajude com esta tarefa usando esta skill.
```

---

### `web-development-design-ops`

**Arquivo:** [`.hermes/skills/forumtelecom/web-development-design-ops/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/forumtelecom/web-development-design-ops/SKILL.md)

**O que faz:** Use when the user asks to create, improve, audit, or deploy high-quality custom websites, landing pages, institutional pages, dashboards, portals, or exclusive web interfaces with strong design, performance, SEO, accessibility, responsive layout, clean HTML/CSS/JS or modern frontend stacks, visual QA, Lighthouse-style validation and production-ready delivery.

**Tags:** `web-development`, `web-design`, `frontend`, `landing-page`, `html`, `css`, `javascript`, `performance`, `seo`, `accessibility`

**Quando usar:**

- criar site institucional, landing page, página de produto ou página comercial;
- criar página personalizada para provedor, telecom, NOC, consultoria, SaaS ou evento;
- melhorar design de HTML/CSS existente;
- criar dashboard/portal web visualmente profissional;
- transformar briefing em layout e código;

**Como acionar no Hermes:**

```text
/skill web-development-design-ops
Me ajude com esta tarefa usando esta skill.
```

**Validação típica:**

- briefing/objetivo entendido;
- direção visual definida;
- layout responsivo implementado;
- SEO básico presente;

---

### `zabbix-ops`

**Arquivo:** [`.hermes/skills/forumtelecom/zabbix-ops/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/forumtelecom/zabbix-ops/SKILL.md)

**O que faz:** Senior Zabbix engineer for monitoring infrastructure (network devices, servers, containers) and creating templates programmatically while respecting API rate limits. Use when the user asks to query, configure, or troubleshoot Zabbix hosts, items, triggers, templates, problems, or maintenance windows; or to create/import templates in bulk respecting PHP-FPM and Postgres lock limits. Triggers include Zabbix, "zabbix api", "zabbix trigger", "zabbix template", "zabbix host", "zabbix problem", "zabbix maintenance", "zabbix snmp", "host está em problema", "criar template Zabbix", "criar template em massa", "import template Zabbix", "rate limit zabbix", "template.massadd", "configuration.import", Zabbix 6.x, Zabbix 7.x.

**Quando usar:**

- Senior Zabbix engineer for monitoring infrastructure (network devices, servers, containers) and creating templates programmatically while respecting API rate limits. Use when the user asks to query, configure, or troubleshoot Zabbix hosts, items, triggers, templates, problems, or maintenance windows; or to create/import templates in bulk respecting PHP-FPM and Postgres lock limits. Triggers include Zabbix, "zabbix api", "zabbix trigger", "zabbix template", "zabbix host", "zabbix problem", "zabbix maintenance", "zabbix snmp", "host está em problema", "criar template Zabbix", "criar template em massa", "import template Zabbix", "rate limit zabbix", "template.massadd", "configuration.import", Zabbix 6.x, Zabbix 7.x.

**Como acionar no Hermes:**

```text
/skill zabbix-ops
Crie um template/dashboard customizado para monitorar este equipamento.
```

---

## Manutenção deste catálogo

Sempre que adicionar uma nova skill, regenere/atualize esta página lendo os `SKILL.md` para manter descrição, caminho e exemplo de uso sincronizados.
