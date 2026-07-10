# Catálogo de Skills Hermes

Página gerada a partir de todos os `SKILL.md` deste repositório. Use como guia operacional para escolher, instalar e acionar cada skill.

## Instalação

Instalar todas as skills:

```bash
git clone https://github.com/clfigueiredo/hermes-infra-skills.git
cd hermes-infra-skills
mkdir -p ~/.hermes/skills
cp -a .hermes/skills/forumtelecom ~/.hermes/skills/
cp -a .hermes/skills/curso-hermes ~/.hermes/skills/
```

Instalar só as skills operacionais dos alunos:

```bash
mkdir -p ~/.hermes/skills
cp -a .hermes/skills/curso-hermes ~/.hermes/skills/
```

Depois, dentro do Hermes:
```text
/reload-skills
```

## Como usar uma skill

```text
/skill nome-da-skill
```

Exemplo:
```text
/skill react-patterns
Crie esta tela e valide build/teste.
```

## Visão geral

| Pasta | Quantidade | Finalidade |
|---|---:|---|
| `curso-hermes/` | 71 | Skills operacionais para alunos: vibe coding, frontend, backend, segurança, testes, deploy, GitHub, MCP e agentes convertidos. |
| `forumtelecom/` | 28 | Skills operacionais para infraestrutura, redes, telecom, virtualização, firewall, monitoramento e sistemas. |

## Índice rápido

| Skill | Pasta | Para que serve |
|---|---|---|
| [`active-directory-automation`](#active-directory-automation) | `curso-hermes/` | Automatizar criação de usuários AD, grupos, compartilhamentos SMB e permissões NTFS com PowerShell seguro. |
| [`accessibility`](#accessibility) | `curso-hermes/` | Design, implement, and audit inclusive digital products using WCAG 2.2 Level AA standards. Use this skill to generate semantic ARIA for Web and accessibility traits for Web and Native platforms (iOS/Android). |
| [`agent-build-error-resolver`](#agent-build-error-resolver) | `curso-hermes/` | Use quando o aluno precisar do comportamento operacional do agente ECC `build-error-resolver`. Build and TypeScript error resolution specialist. Use PROACTIVELY when build fails or type errors occur. Fixes build/type errors only with minimal diffs, no architectural edits. Focuses on getting the build green quickly. |
| [`agent-code-architect`](#agent-code-architect) | `curso-hermes/` | Use quando o aluno precisar do comportamento operacional do agente ECC `code-architect`. Designs feature architectures by analyzing existing codebase patterns and conventions, then providing implementation blueprints with concrete files, interfaces, data flow, and build order. |
| [`agent-code-explorer`](#agent-code-explorer) | `curso-hermes/` | Use quando o aluno precisar do comportamento operacional do agente ECC `code-explorer`. Deeply analyzes existing codebase features by tracing execution paths, mapping architecture layers, and documenting dependencies to inform new development. |
| [`agent-code-reviewer`](#agent-code-reviewer) | `curso-hermes/` | Use quando o aluno precisar do comportamento operacional do agente ECC `code-reviewer`. Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code. MUST BE USED for all code changes. |
| [`agent-code-simplifier`](#agent-code-simplifier) | `curso-hermes/` | Use quando o aluno precisar do comportamento operacional do agente ECC `code-simplifier`. Simplifies and refines code for clarity, consistency, and maintainability while preserving behavior. Focus on recently modified code unless instructed otherwise. |
| [`agent-database-reviewer`](#agent-database-reviewer) | `curso-hermes/` | Use quando o aluno precisar do comportamento operacional do agente ECC `database-reviewer`. PostgreSQL database specialist for query optimization, schema design, security, and performance. Use PROACTIVELY when writing SQL, creating migrations, designing schemas, or troubleshooting database performance. Incorporates Supabase best practices. |
| [`agent-docs-lookup`](#agent-docs-lookup) | `curso-hermes/` | Use quando o aluno precisar do comportamento operacional do agente ECC `docs-lookup`. When the user asks how to use a library, framework, or API or needs up-to-date code examples, use Context7 MCP to fetch current documentation and return answers with examples. Invoke for docs/API/setup questions. |
| [`agent-e2e-runner`](#agent-e2e-runner) | `curso-hermes/` | Use quando o aluno precisar do comportamento operacional do agente ECC `e2e-runner`. End-to-end testing specialist using Vercel Agent Browser (preferred) with Playwright fallback. Use PROACTIVELY for generating, maintaining, and running E2E tests. Manages test journeys, quarantines flaky tests, uploads artifacts (screenshots, videos, traces), and ensures critical user flows work. |
| [`agent-fastapi-reviewer`](#agent-fastapi-reviewer) | `curso-hermes/` | Use quando o aluno precisar do comportamento operacional do agente ECC `fastapi-reviewer`. Reviews FastAPI applications for async correctness, dependency injection, Pydantic schemas, security, OpenAPI quality, testing, and production readiness. |
| [`agent-performance-optimizer`](#agent-performance-optimizer) | `curso-hermes/` | Use quando o aluno precisar do comportamento operacional do agente ECC `performance-optimizer`. Performance analysis and optimization specialist. Use PROACTIVELY for identifying bottlenecks, optimizing slow code, reducing bundle sizes, and improving runtime performance. Profiling, memory leaks, render optimization, and algorithmic improvements. |
| [`agent-planner`](#agent-planner) | `curso-hermes/` | Use quando o aluno precisar do comportamento operacional do agente ECC `planner`. Expert planning specialist for complex features and refactoring. Use PROACTIVELY when users request feature implementation, architectural changes, or complex refactoring. Automatically activated for planning tasks. |
| [`agent-pr-test-analyzer`](#agent-pr-test-analyzer) | `curso-hermes/` | Use quando o aluno precisar do comportamento operacional do agente ECC `pr-test-analyzer`. Review pull request test coverage quality and completeness, with emphasis on behavioral coverage and real bug prevention. |
| [`agent-python-reviewer`](#agent-python-reviewer) | `curso-hermes/` | Use quando o aluno precisar do comportamento operacional do agente ECC `python-reviewer`. Expert Python code reviewer specializing in PEP 8 compliance, Pythonic idioms, type hints, security, and performance. Use for all Python code changes. MUST BE USED for Python projects. |
| [`agent-react-build-resolver`](#agent-react-build-resolver) | `curso-hermes/` | Use quando o aluno precisar do comportamento operacional do agente ECC `react-build-resolver`. Diagnose and fix React build failures across Vite, webpack, Next.js, CRA, Parcel, esbuild, and Bun. Handles JSX/TSX compile errors, hydration mismatches, server/client component boundary failures, missing types, and bundler-specific configuration issues with minimal, surgical changes. MUST BE USED when a React build fails. |
| [`agent-react-reviewer`](#agent-react-reviewer) | `curso-hermes/` | Use quando o aluno precisar do comportamento operacional do agente ECC `react-reviewer`. Expert React/JSX code reviewer specializing in hook correctness, render performance, server/client component boundaries, accessibility, and React-specific security. Use for any change touching .tsx/.jsx files or React component logic. MUST BE USED for React projects. |
| [`agent-security-reviewer`](#agent-security-reviewer) | `curso-hermes/` | Use quando o aluno precisar do comportamento operacional do agente ECC `security-reviewer`. Security vulnerability detection and remediation specialist. Use PROACTIVELY after writing code that handles user input, authentication, API endpoints, or sensitive data. Flags secrets, SSRF, injection, unsafe crypto, and OWASP Top 10 vulnerabilities. |
| [`agent-tdd-guide`](#agent-tdd-guide) | `curso-hermes/` | Use quando o aluno precisar do comportamento operacional do agente ECC `tdd-guide`. Test-Driven Development specialist enforcing write-tests-first methodology. Use PROACTIVELY when writing new features, fixing bugs, or refactoring code. Ensures 80%+ test coverage. |
| [`agent-typescript-reviewer`](#agent-typescript-reviewer) | `curso-hermes/` | Use quando o aluno precisar do comportamento operacional do agente ECC `typescript-reviewer`. Expert TypeScript/JavaScript code reviewer specializing in type safety, async correctness, Node/web security, and idiomatic patterns. Use for all TypeScript and JavaScript code changes. MUST BE USED for TypeScript/JavaScript projects. |
| [`ai-regression-testing`](#ai-regression-testing) | `curso-hermes/` | Regression testing strategies for AI-assisted development. Sandbox-mode API testing without database dependencies, automated bug-check workflows, and patterns to catch AI blind spots where the same model writes and reviews code. |
| [`api-design`](#api-design) | `curso-hermes/` | REST API design patterns including resource naming, status codes, pagination, filtering, error responses, versioning, and rate limiting for production APIs. |
| [`backend-api-patterns`](#backend-api-patterns) | `curso-hermes/` | Use quando o aluno estiver criando ou revisando backend/API. Cobre rotas REST, camada service/repository, validação, erros HTTP, autenticação, rate limit, paginação, logs e contrato entre frontend/backend. |
| [`backend-patterns`](#backend-patterns) | `curso-hermes/` | Backend architecture patterns, API design, database optimization, and server-side best practices for Node.js, Express, and Next.js API routes. |
| [`browser-qa`](#browser-qa) | `curso-hermes/` | Use this skill to automate visual testing and UI interaction verification using browser automation after deploying features. |
| [`caveman-terse-mode`](#caveman-terse-mode) | `curso-hermes/` | Use quando o aluno quiser reduzir tokens/verbosidade do Hermes Agent sem perder conteúdo técnico. Ativa um modo de resposta ultra objetivo em PT-BR ou no idioma do usuário, preservando comandos, código, erros, nomes de APIs e avisos críticos. Inclui padrões para resposta curta, mensagens de commit, revisão de código e compressão segura de textos de memória/instruções. |
| [`codebase-onboarding`](#codebase-onboarding) | `curso-hermes/` | Analyze an unfamiliar codebase and generate a structured onboarding guide with architecture map, key entry points, conventions, and a starter CLAUDE.md. Use when joining a new project or setting up Claude Code for the first time in a repo. |
| [`database-migrations`](#database-migrations) | `curso-hermes/` | Database migration best practices for schema changes, data migrations, rollbacks, and zero-downtime deployments across PostgreSQL, MySQL, and common ORMs (Prisma, Drizzle, Kysely, Django, TypeORM, golang-migrate). |
| [`database-postgres-prisma`](#database-postgres-prisma) | `curso-hermes/` | Use quando o aluno estiver modelando banco, criando migrations, usando PostgreSQL/MySQL/Prisma ou investigando lentidão/erro de query. Foca em schema simples, índices, transações, paginação e migração segura. |
| [`deployment-patterns`](#deployment-patterns) | `curso-hermes/` | Deployment workflows, CI/CD pipeline patterns, Docker containerization, health checks, rollback strategies, and production readiness checklists for web applications. |
| [`design-system`](#design-system) | `curso-hermes/` | Use this skill to generate or audit design systems, check visual consistency, and review PRs that touch styling. |
| [`django-patterns`](#django-patterns) | `curso-hermes/` | Django architecture patterns, REST API design with DRF, ORM best practices, caching, signals, middleware, and production-grade Django apps. |
| [`django-security`](#django-security) | `curso-hermes/` | Django security best practices, authentication, authorization, CSRF protection, SQL injection prevention, XSS prevention, and secure deployment configurations. |
| [`django-tdd`](#django-tdd) | `curso-hermes/` | Django testing strategies with pytest-django, TDD methodology, factory_boy, mocking, coverage, and testing Django REST Framework APIs. |
| [`django-verification`](#django-verification) | `curso-hermes/` | Verification loop for Django projects: migrations, linting, tests with coverage, security scans, and deployment readiness checks before release or PR. |
| [`docker-deploy-basics`](#docker-deploy-basics) | `curso-hermes/` | Use quando o aluno quiser containerizar ou publicar uma aplicação. Cobre Dockerfile simples, Compose, variáveis de ambiente, healthcheck, logs, rollback básico e validação pós-deploy. |
| [`docker-patterns`](#docker-patterns) | `curso-hermes/` | Docker and Docker Compose patterns for local development, container security, networking, volume strategies, and multi-service orchestration. |
| [`documentation-lookup`](#documentation-lookup) | `curso-hermes/` | Use up-to-date library and framework docs via Context7 MCP instead of training data. Activates for setup questions, API references, code examples, or when the user names a framework (e.g. React, Next.js, Prisma). |
| [`e2e-testing`](#e2e-testing) | `curso-hermes/` | Playwright E2E testing patterns, Page Object Model, configuration, CI/CD integration, artifact management, and flaky test strategies. |
| [`error-handling`](#error-handling) | `curso-hermes/` | Patterns for robust error handling across TypeScript, Python, and Go. Covers typed errors, error boundaries, retries, circuit breakers, and user-facing error messages. |
| [`fastapi-patterns`](#fastapi-patterns) | `curso-hermes/` | FastAPI best practices covering project structure, Pydantic v2 schemas, dependency injection, async handlers, authentication, authorization, transactional service layers, and testing with httpx and pytest. |
| [`frontend-a11y`](#frontend-a11y) | `curso-hermes/` | Accessibility patterns for React and Next.js — semantic HTML, ARIA attributes, form labeling, keyboard navigation, focus management, and screen reader support. Use when building any interactive UI component or form. |
| [`frontend-browser-qa`](#frontend-browser-qa) | `curso-hermes/` | Use quando o aluno precisar validar visualmente uma aplicação web. Define fluxo de QA com navegador: abrir app, testar caminho feliz, estados de erro/vazio, responsividade, console, network e acessibilidade básica. |
| [`frontend-design-direction`](#frontend-design-direction) | `curso-hermes/` | Set an ECC-specific frontend design direction for production UI work. Use when building or improving websites, dashboards, applications, components, landing pages, visual tools, or any web UI that needs stronger product-specific design judgment. |
| [`frontend-patterns`](#frontend-patterns) | `curso-hermes/` | Frontend development patterns for React, Next.js, state management, performance optimization, and UI best practices. |
| [`frontend-react-nextjs`](#frontend-react-nextjs) | `curso-hermes/` | Use quando o aluno estiver criando ou revisando frontend React/Next.js. Cobre componentes, estado, forms, acessibilidade, performance, responsividade, UX e build sem transformar o projeto em arquitetura exagerada. |
| [`git-workflow`](#git-workflow) | `curso-hermes/` | Git workflow patterns including branching strategies, commit conventions, merge vs rebase, conflict resolution, and collaborative development best practices for teams of all sizes. |
| [`github-ops`](#github-ops) | `curso-hermes/` | GitHub repository operations, automation, and management. Issue triage, PR management, CI/CD operations, release management, and security monitoring using the gh CLI. Use when the user wants to manage GitHub issues, PRs, CI status, releases, contributors, stale items, or any GitHub operational task beyond simple git commands. |
| [`github-workflow-student`](#github-workflow-student) | `curso-hermes/` | Use quando o aluno trabalhar com GitHub: criar repo, commits, branches, pull requests, issues, releases e CI básico. Foca em fluxo seguro e simples para projetos de estudo e MVPs. |
| [`hexagonal-architecture`](#hexagonal-architecture) | `curso-hermes/` | Design, implement, and refactor Ports & Adapters systems with clear domain boundaries, dependency inversion, and testable use-case orchestration across TypeScript, Java, Kotlin, and Go services. |
| [`laravel-patterns`](#laravel-patterns) | `curso-hermes/` | Laravel architecture patterns, routing/controllers, Eloquent ORM, service layers, queues, events, caching, and API resources for production apps. |
| [`laravel-security`](#laravel-security) | `curso-hermes/` | Laravel security best practices — authentication, authorization, Eloquent safety, CSRF, XSS prevention, API security, and secure deployment configurations. |
| [`laravel-tdd`](#laravel-tdd) | `curso-hermes/` | Laravel testing strategies with PHPUnit, Pest, model factories, HTTP tests, Sanctum authentication testing, mocking, and coverage. |
| [`laravel-verification`](#laravel-verification) | `curso-hermes/` | Verification loop for Laravel projects: env checks, linting, static analysis, tests with coverage, security scans, and deployment readiness. |
| [`mcp-server-builder`](#mcp-server-builder) | `curso-hermes/` | Use quando o aluno quiser criar um MCP server para Hermes/agents. Orienta design de tools, schemas, validação, stdio/HTTP, segurança, testes locais e documentação mínima. |
| [`mcp-server-patterns`](#mcp-server-patterns) | `curso-hermes/` | Build MCP servers with Node/TypeScript SDK — tools, resources, prompts, Zod validation, stdio vs Streamable HTTP. Use Context7 or official MCP docs for latest API. |
| [`mysql-patterns`](#mysql-patterns) | `curso-hermes/` | MySQL and MariaDB schema, query, indexing, transaction, replication, and connection-pool patterns for production backends. |
| [`nestjs-patterns`](#nestjs-patterns) | `curso-hermes/` | NestJS architecture patterns for modules, controllers, providers, DTO validation, guards, interceptors, config, and production-grade TypeScript backends. |
| [`nextjs-turbopack`](#nextjs-turbopack) | `curso-hermes/` | Next.js 16+ and Turbopack — incremental bundling, FS caching, dev speed, and when to use Turbopack vs webpack. |
| [`postgres-patterns`](#postgres-patterns) | `curso-hermes/` | PostgreSQL database patterns for query optimization, schema design, indexing, and security. Based on Supabase best practices. |
| [`prisma-patterns`](#prisma-patterns) | `curso-hermes/` | Prisma ORM patterns for TypeScript backends — schema design, query optimization, transactions, pagination, and critical traps like updateMany returning count not records, $transaction timeouts, migrate dev resetting the DB, @updatedAt skipped on bulk writes, and serverless connection exhaustion. |
| [`python-patterns`](#python-patterns) | `curso-hermes/` | Pythonic idioms, PEP 8 standards, type hints, and best practices for building robust, efficient, and maintainable Python applications. |
| [`python-testing`](#python-testing) | `curso-hermes/` | Python testing strategies using pytest, TDD methodology, fixtures, mocking, parametrization, and coverage requirements. |
| [`react-patterns`](#react-patterns) | `curso-hermes/` | React 18/19 patterns including hooks discipline, server/client component boundaries, Suspense + error boundaries, form actions, data fetching, state management decision trees, and accessibility-first composition. Use when writing or reviewing React components. |
| [`react-performance`](#react-performance) | `curso-hermes/` | React and Next.js performance optimization patterns adapted from Vercel Engineering's React Best Practices (https://github.com/vercel-labs/agent-skills). Organizes 70+ rules across 8 priority categories — waterfalls, bundle size, server-side, client fetching, re-render, rendering, JS micro-perf, advanced. Use when writing, reviewing, or refactoring React/Next.js code for performance. |
| [`react-testing`](#react-testing) | `curso-hermes/` | React component testing with React Testing Library, Vitest/Jest, MSW for network mocking, accessibility assertions with axe, and the decision boundary between component tests and Playwright/Cypress end-to-end runs. Use when writing or fixing tests for React components, hooks, or pages. |
| [`security-review`](#security-review) | `curso-hermes/` | Use this skill when adding authentication, handling user input, working with secrets, creating API endpoints, or implementing payment/sensitive features. Provides comprehensive security checklist and patterns. |
| [`security-review-webapp`](#security-review-webapp) | `curso-hermes/` | Use quando o aluno criar autenticação, API, upload, pagamento, painel admin, integração externa ou qualquer código com dados sensíveis. Aplica checklist prático de segurança web antes de publicar. |
| [`tdd-workflow`](#tdd-workflow) | `curso-hermes/` | Use this skill when writing new features, fixing bugs, or refactoring code. Enforces test-driven development with 80%+ coverage including unit, integration, and E2E tests. |
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

## Curso Hermes / Operacional para alunos

### `active-directory-automation`

**Arquivo:** [`.hermes/skills/curso-hermes/active-directory-automation/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/active-directory-automation/SKILL.md)

**O que faz:** Automatiza tarefas de Active Directory com PowerShell de forma segura: criação de usuários, grupos, liberação de pastas/compartilhamentos SMB e permissões NTFS.

**Tags:** `curso-hermes`, `active-directory`, `windows-server`, `powershell`, `smb`, `ntfs`, `automation`

**Quando usar:**
- Criar usuários no Active Directory com validação e senha inicial segura.
- Adicionar usuário a grupos e conferir associação.
- Criar/liberar pastas de rede com permissões SMB e NTFS.
- Gerar script PowerShell idempotente para automação AD.

**Como acionar no Hermes:**
```text
/skill active-directory-automation
Monte uma automação para criar usuário AD, adicionar grupos e liberar pasta de rede.
```

---

### `accessibility`

**Arquivo:** [`.hermes/skills/curso-hermes/accessibility/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/accessibility/SKILL.md)

**O que faz:** Design, implement, and audit inclusive digital products using WCAG 2.2 Level AA standards. Use this skill to generate semantic ARIA for Web and accessibility traits for Web and Native platforms (iOS/Android).

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Defining UI component specifications for Web, iOS, or Android.
- Auditing existing code for accessibility barriers or compliance gaps.
- Implementing new WCAG 2.2 standards like Target Size (Minimum) and Focus Appearance.
- Mapping high-level design requirements to technical attributes (ARIA roles, traits, hints).

**Como acionar no Hermes:**
```text
/skill accessibility
Execute esta tarefa usando esta skill e valide o resultado.
```

---

### `agent-build-error-resolver`

**Arquivo:** [`.hermes/skills/curso-hermes/agent-build-error-resolver/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/agent-build-error-resolver/SKILL.md)

**O que faz:** Use quando o aluno precisar do comportamento operacional do agente ECC `build-error-resolver`. Build and TypeScript error resolution specialist. Use PROACTIVELY when build fails or type errors occur. Fixes build/type errors only with minimal diffs, no architectural edits. Focuses on getting the build green quickly.

**Tags:** `curso-hermes`, `operational`, `ecc`, `converted-agent`

**Quando usar:**
- Use quando o aluno precisar do comportamento operacional do agente ECC `build-error-resolver`. Build and TypeScript error resolution specialist. Use PROACTIVELY when build fails or type errors occur. Fixes build/type errors only with minimal diffs, no architectural edits. Focuses on getting the build green quickly.

**Como acionar no Hermes:**
```text
/skill agent-build-error-resolver
Atue com este agente operacional sobre o arquivo/diff/erro informado.
```

---

### `agent-code-architect`

**Arquivo:** [`.hermes/skills/curso-hermes/agent-code-architect/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/agent-code-architect/SKILL.md)

**O que faz:** Use quando o aluno precisar do comportamento operacional do agente ECC `code-architect`. Designs feature architectures by analyzing existing codebase patterns and conventions, then providing implementation blueprints with concrete files, interfaces, data flow, and build order.

**Tags:** `curso-hermes`, `operational`, `ecc`, `converted-agent`

**Quando usar:**
- Use quando o aluno precisar do comportamento operacional do agente ECC `code-architect`. Designs feature architectures by analyzing existing codebase patterns and conventions, then providing implementation blueprints with concrete files, interfaces, data flow, and build order.

**Como acionar no Hermes:**
```text
/skill agent-code-architect
Atue com este agente operacional sobre o arquivo/diff/erro informado.
```

---

### `agent-code-explorer`

**Arquivo:** [`.hermes/skills/curso-hermes/agent-code-explorer/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/agent-code-explorer/SKILL.md)

**O que faz:** Use quando o aluno precisar do comportamento operacional do agente ECC `code-explorer`. Deeply analyzes existing codebase features by tracing execution paths, mapping architecture layers, and documenting dependencies to inform new development.

**Tags:** `curso-hermes`, `operational`, `ecc`, `converted-agent`

**Quando usar:**
- Use quando o aluno precisar do comportamento operacional do agente ECC `code-explorer`. Deeply analyzes existing codebase features by tracing execution paths, mapping architecture layers, and documenting dependencies to inform new development.

**Como acionar no Hermes:**
```text
/skill agent-code-explorer
Atue com este agente operacional sobre o arquivo/diff/erro informado.
```

---

### `agent-code-reviewer`

**Arquivo:** [`.hermes/skills/curso-hermes/agent-code-reviewer/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/agent-code-reviewer/SKILL.md)

**O que faz:** Use quando o aluno precisar do comportamento operacional do agente ECC `code-reviewer`. Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code. MUST BE USED for all code changes.

**Tags:** `curso-hermes`, `operational`, `ecc`, `converted-agent`

**Quando usar:**
- Use quando o aluno precisar do comportamento operacional do agente ECC `code-reviewer`. Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code. MUST BE USED for all code changes.

**Como acionar no Hermes:**
```text
/skill agent-code-reviewer
Atue com este agente operacional sobre o arquivo/diff/erro informado.
```

---

### `agent-code-simplifier`

**Arquivo:** [`.hermes/skills/curso-hermes/agent-code-simplifier/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/agent-code-simplifier/SKILL.md)

**O que faz:** Use quando o aluno precisar do comportamento operacional do agente ECC `code-simplifier`. Simplifies and refines code for clarity, consistency, and maintainability while preserving behavior. Focus on recently modified code unless instructed otherwise.

**Tags:** `curso-hermes`, `operational`, `ecc`, `converted-agent`

**Quando usar:**
- Use quando o aluno precisar do comportamento operacional do agente ECC `code-simplifier`. Simplifies and refines code for clarity, consistency, and maintainability while preserving behavior. Focus on recently modified code unless instructed otherwise.

**Como acionar no Hermes:**
```text
/skill agent-code-simplifier
Atue com este agente operacional sobre o arquivo/diff/erro informado.
```

---

### `agent-database-reviewer`

**Arquivo:** [`.hermes/skills/curso-hermes/agent-database-reviewer/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/agent-database-reviewer/SKILL.md)

**O que faz:** Use quando o aluno precisar do comportamento operacional do agente ECC `database-reviewer`. PostgreSQL database specialist for query optimization, schema design, security, and performance. Use PROACTIVELY when writing SQL, creating migrations, designing schemas, or troubleshooting database performance. Incorporates Supabase best practices.

**Tags:** `curso-hermes`, `operational`, `ecc`, `converted-agent`

**Quando usar:**
- Use quando o aluno precisar do comportamento operacional do agente ECC `database-reviewer`. PostgreSQL database specialist for query optimization, schema design, security, and performance. Use PROACTIVELY when writing SQL, creating migrations, designing schemas, or troubleshooting database performance. Incorporates Supabase best practices.

**Como acionar no Hermes:**
```text
/skill agent-database-reviewer
Atue com este agente operacional sobre o arquivo/diff/erro informado.
```

---

### `agent-docs-lookup`

**Arquivo:** [`.hermes/skills/curso-hermes/agent-docs-lookup/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/agent-docs-lookup/SKILL.md)

**O que faz:** Use quando o aluno precisar do comportamento operacional do agente ECC `docs-lookup`. When the user asks how to use a library, framework, or API or needs up-to-date code examples, use Context7 MCP to fetch current documentation and return answers with examples. Invoke for docs/API/setup questions.

**Tags:** `curso-hermes`, `operational`, `ecc`, `converted-agent`

**Quando usar:**
- Use quando o aluno precisar do comportamento operacional do agente ECC `docs-lookup`. When the user asks how to use a library, framework, or API or needs up-to-date code examples, use Context7 MCP to fetch current documentation and return answers with examples. Invoke for docs/API/setup questions.

**Como acionar no Hermes:**
```text
/skill agent-docs-lookup
Atue com este agente operacional sobre o arquivo/diff/erro informado.
```

---

### `agent-e2e-runner`

**Arquivo:** [`.hermes/skills/curso-hermes/agent-e2e-runner/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/agent-e2e-runner/SKILL.md)

**O que faz:** Use quando o aluno precisar do comportamento operacional do agente ECC `e2e-runner`. End-to-end testing specialist using Vercel Agent Browser (preferred) with Playwright fallback. Use PROACTIVELY for generating, maintaining, and running E2E tests. Manages test journeys, quarantines flaky tests, uploads artifacts (screenshots, videos, traces), and ensures critical user flows work.

**Tags:** `curso-hermes`, `operational`, `ecc`, `converted-agent`

**Quando usar:**
- Use quando o aluno precisar do comportamento operacional do agente ECC `e2e-runner`. End-to-end testing specialist using Vercel Agent Browser (preferred) with Playwright fallback. Use PROACTIVELY for generating, maintaining, and running E2E tests. Manages test journeys, quarantines flaky tests, uploads artifacts (screenshots, videos, traces), and ensures critical user flows work.

**Como acionar no Hermes:**
```text
/skill agent-e2e-runner
Atue com este agente operacional sobre o arquivo/diff/erro informado.
```

---

### `agent-fastapi-reviewer`

**Arquivo:** [`.hermes/skills/curso-hermes/agent-fastapi-reviewer/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/agent-fastapi-reviewer/SKILL.md)

**O que faz:** Use quando o aluno precisar do comportamento operacional do agente ECC `fastapi-reviewer`. Reviews FastAPI applications for async correctness, dependency injection, Pydantic schemas, security, OpenAPI quality, testing, and production readiness.

**Tags:** `curso-hermes`, `operational`, `ecc`, `converted-agent`

**Quando usar:**
- Use quando o aluno precisar do comportamento operacional do agente ECC `fastapi-reviewer`. Reviews FastAPI applications for async correctness, dependency injection, Pydantic schemas, security, OpenAPI quality, testing, and production readiness.

**Como acionar no Hermes:**
```text
/skill agent-fastapi-reviewer
Atue com este agente operacional sobre o arquivo/diff/erro informado.
```

---

### `agent-performance-optimizer`

**Arquivo:** [`.hermes/skills/curso-hermes/agent-performance-optimizer/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/agent-performance-optimizer/SKILL.md)

**O que faz:** Use quando o aluno precisar do comportamento operacional do agente ECC `performance-optimizer`. Performance analysis and optimization specialist. Use PROACTIVELY for identifying bottlenecks, optimizing slow code, reducing bundle sizes, and improving runtime performance. Profiling, memory leaks, render optimization, and algorithmic improvements.

**Tags:** `curso-hermes`, `operational`, `ecc`, `converted-agent`

**Quando usar:**
- Use quando o aluno precisar do comportamento operacional do agente ECC `performance-optimizer`. Performance analysis and optimization specialist. Use PROACTIVELY for identifying bottlenecks, optimizing slow code, reducing bundle sizes, and improving runtime performance. Profiling, memory leaks, render optimization, and algorithmic improvements.

**Como acionar no Hermes:**
```text
/skill agent-performance-optimizer
Atue com este agente operacional sobre o arquivo/diff/erro informado.
```

---

### `agent-planner`

**Arquivo:** [`.hermes/skills/curso-hermes/agent-planner/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/agent-planner/SKILL.md)

**O que faz:** Use quando o aluno precisar do comportamento operacional do agente ECC `planner`. Expert planning specialist for complex features and refactoring. Use PROACTIVELY when users request feature implementation, architectural changes, or complex refactoring. Automatically activated for planning tasks.

**Tags:** `curso-hermes`, `operational`, `ecc`, `converted-agent`

**Quando usar:**
- Use quando o aluno precisar do comportamento operacional do agente ECC `planner`. Expert planning specialist for complex features and refactoring. Use PROACTIVELY when users request feature implementation, architectural changes, or complex refactoring. Automatically activated for planning tasks.

**Como acionar no Hermes:**
```text
/skill agent-planner
Atue com este agente operacional sobre o arquivo/diff/erro informado.
```

---

### `agent-pr-test-analyzer`

**Arquivo:** [`.hermes/skills/curso-hermes/agent-pr-test-analyzer/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/agent-pr-test-analyzer/SKILL.md)

**O que faz:** Use quando o aluno precisar do comportamento operacional do agente ECC `pr-test-analyzer`. Review pull request test coverage quality and completeness, with emphasis on behavioral coverage and real bug prevention.

**Tags:** `curso-hermes`, `operational`, `ecc`, `converted-agent`

**Quando usar:**
- Use quando o aluno precisar do comportamento operacional do agente ECC `pr-test-analyzer`. Review pull request test coverage quality and completeness, with emphasis on behavioral coverage and real bug prevention.

**Como acionar no Hermes:**
```text
/skill agent-pr-test-analyzer
Atue com este agente operacional sobre o arquivo/diff/erro informado.
```

---

### `agent-python-reviewer`

**Arquivo:** [`.hermes/skills/curso-hermes/agent-python-reviewer/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/agent-python-reviewer/SKILL.md)

**O que faz:** Use quando o aluno precisar do comportamento operacional do agente ECC `python-reviewer`. Expert Python code reviewer specializing in PEP 8 compliance, Pythonic idioms, type hints, security, and performance. Use for all Python code changes. MUST BE USED for Python projects.

**Tags:** `curso-hermes`, `operational`, `ecc`, `converted-agent`

**Quando usar:**
- Use quando o aluno precisar do comportamento operacional do agente ECC `python-reviewer`. Expert Python code reviewer specializing in PEP 8 compliance, Pythonic idioms, type hints, security, and performance. Use for all Python code changes. MUST BE USED for Python projects.

**Como acionar no Hermes:**
```text
/skill agent-python-reviewer
Atue com este agente operacional sobre o arquivo/diff/erro informado.
```

---

### `agent-react-build-resolver`

**Arquivo:** [`.hermes/skills/curso-hermes/agent-react-build-resolver/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/agent-react-build-resolver/SKILL.md)

**O que faz:** Use quando o aluno precisar do comportamento operacional do agente ECC `react-build-resolver`. Diagnose and fix React build failures across Vite, webpack, Next.js, CRA, Parcel, esbuild, and Bun. Handles JSX/TSX compile errors, hydration mismatches, server/client component boundary failures, missing types, and bundler-specific configuration issues with minimal, surgical changes. MUST BE USED when a React build fails.

**Tags:** `curso-hermes`, `operational`, `ecc`, `converted-agent`

**Quando usar:**
- Use quando o aluno precisar do comportamento operacional do agente ECC `react-build-resolver`. Diagnose and fix React build failures across Vite, webpack, Next.js, CRA, Parcel, esbuild, and Bun. Handles JSX/TSX compile errors, hydration mismatches, server/client component boundary failures, missing types, and bundler-specific configuration issues with minimal, surgical changes. MUST BE USED when a React build fails.

**Como acionar no Hermes:**
```text
/skill agent-react-build-resolver
Atue com este agente operacional sobre o arquivo/diff/erro informado.
```

---

### `agent-react-reviewer`

**Arquivo:** [`.hermes/skills/curso-hermes/agent-react-reviewer/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/agent-react-reviewer/SKILL.md)

**O que faz:** Use quando o aluno precisar do comportamento operacional do agente ECC `react-reviewer`. Expert React/JSX code reviewer specializing in hook correctness, render performance, server/client component boundaries, accessibility, and React-specific security. Use for any change touching .tsx/.jsx files or React component logic. MUST BE USED for React projects.

**Tags:** `curso-hermes`, `operational`, `ecc`, `converted-agent`

**Quando usar:**
- Use quando o aluno precisar do comportamento operacional do agente ECC `react-reviewer`. Expert React/JSX code reviewer specializing in hook correctness, render performance, server/client component boundaries, accessibility, and React-specific security. Use for any change touching .tsx/.jsx files or React component logic. MUST BE USED for React projects.

**Como acionar no Hermes:**
```text
/skill agent-react-reviewer
Atue com este agente operacional sobre o arquivo/diff/erro informado.
```

---

### `agent-security-reviewer`

**Arquivo:** [`.hermes/skills/curso-hermes/agent-security-reviewer/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/agent-security-reviewer/SKILL.md)

**O que faz:** Use quando o aluno precisar do comportamento operacional do agente ECC `security-reviewer`. Security vulnerability detection and remediation specialist. Use PROACTIVELY after writing code that handles user input, authentication, API endpoints, or sensitive data. Flags secrets, SSRF, injection, unsafe crypto, and OWASP Top 10 vulnerabilities.

**Tags:** `curso-hermes`, `operational`, `ecc`, `converted-agent`

**Quando usar:**
- Use quando o aluno precisar do comportamento operacional do agente ECC `security-reviewer`. Security vulnerability detection and remediation specialist. Use PROACTIVELY after writing code that handles user input, authentication, API endpoints, or sensitive data. Flags secrets, SSRF, injection, unsafe crypto, and OWASP Top 10 vulnerabilities.

**Como acionar no Hermes:**
```text
/skill agent-security-reviewer
Atue com este agente operacional sobre o arquivo/diff/erro informado.
```

---

### `agent-tdd-guide`

**Arquivo:** [`.hermes/skills/curso-hermes/agent-tdd-guide/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/agent-tdd-guide/SKILL.md)

**O que faz:** Use quando o aluno precisar do comportamento operacional do agente ECC `tdd-guide`. Test-Driven Development specialist enforcing write-tests-first methodology. Use PROACTIVELY when writing new features, fixing bugs, or refactoring code. Ensures 80%+ test coverage.

**Tags:** `curso-hermes`, `operational`, `ecc`, `converted-agent`

**Quando usar:**
- Use quando o aluno precisar do comportamento operacional do agente ECC `tdd-guide`. Test-Driven Development specialist enforcing write-tests-first methodology. Use PROACTIVELY when writing new features, fixing bugs, or refactoring code. Ensures 80%+ test coverage.

**Como acionar no Hermes:**
```text
/skill agent-tdd-guide
Atue com este agente operacional sobre o arquivo/diff/erro informado.
```

---

### `agent-typescript-reviewer`

**Arquivo:** [`.hermes/skills/curso-hermes/agent-typescript-reviewer/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/agent-typescript-reviewer/SKILL.md)

**O que faz:** Use quando o aluno precisar do comportamento operacional do agente ECC `typescript-reviewer`. Expert TypeScript/JavaScript code reviewer specializing in type safety, async correctness, Node/web security, and idiomatic patterns. Use for all TypeScript and JavaScript code changes. MUST BE USED for TypeScript/JavaScript projects.

**Tags:** `curso-hermes`, `operational`, `ecc`, `converted-agent`

**Quando usar:**
- Use quando o aluno precisar do comportamento operacional do agente ECC `typescript-reviewer`. Expert TypeScript/JavaScript code reviewer specializing in type safety, async correctness, Node/web security, and idiomatic patterns. Use for all TypeScript and JavaScript code changes. MUST BE USED for TypeScript/JavaScript projects.

**Como acionar no Hermes:**
```text
/skill agent-typescript-reviewer
Atue com este agente operacional sobre o arquivo/diff/erro informado.
```

---

### `ai-regression-testing`

**Arquivo:** [`.hermes/skills/curso-hermes/ai-regression-testing/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/ai-regression-testing/SKILL.md)

**O que faz:** Regression testing strategies for AI-assisted development. Sandbox-mode API testing without database dependencies, automated bug-check workflows, and patterns to catch AI blind spots where the same model writes and reviews code.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- AI agent (Claude Code, Cursor, Codex) has modified API routes or backend logic
- A bug was found and fixed — need to prevent re-introduction
- Project has a sandbox/mock mode that can be leveraged for DB-free testing
- Running `/bug-check` or similar review commands after code changes
- Multiple code paths exist (sandbox vs production, feature flags, etc.)

**Como acionar no Hermes:**
```text
/skill ai-regression-testing
Crie/rode testes para esta mudança e reporte evidência real.
```

---

### `api-design`

**Arquivo:** [`.hermes/skills/curso-hermes/api-design/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/api-design/SKILL.md)

**O que faz:** REST API design patterns including resource naming, status codes, pagination, filtering, error responses, versioning, and rate limiting for production APIs.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Designing new API endpoints
- Reviewing existing API contracts
- Adding pagination, filtering, or sorting
- Implementing error handling for APIs
- Planning API versioning strategy

**Como acionar no Hermes:**
```text
/skill api-design
Implemente/revise esta API com validação, erros HTTP e testes.
```

---

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
Implemente/revise esta API com validação, erros HTTP e testes.
```

**Validação típica:**
- Input validado por schema
- Erros não vazam stack/segredo
- Auth/permission checada no servidor
- Paginação em listas

---

### `backend-patterns`

**Arquivo:** [`.hermes/skills/curso-hermes/backend-patterns/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/backend-patterns/SKILL.md)

**O que faz:** Backend architecture patterns, API design, database optimization, and server-side best practices for Node.js, Express, and Next.js API routes.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Designing REST or GraphQL API endpoints
- Implementing repository, service, or controller layers
- Optimizing database queries (N+1, indexing, connection pooling)
- Adding caching (Redis, in-memory, HTTP cache headers)
- Setting up background jobs or async processing

**Como acionar no Hermes:**
```text
/skill backend-patterns
Implemente/revise esta API com validação, erros HTTP e testes.
```

---

### `browser-qa`

**Arquivo:** [`.hermes/skills/curso-hermes/browser-qa/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/browser-qa/SKILL.md)

**O que faz:** Use this skill to automate visual testing and UI interaction verification using browser automation after deploying features.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- After deploying a feature to staging/preview
- When you need to verify UI behavior across pages
- Before shipping — confirm layouts, forms, interactions actually work
- When reviewing PRs that touch frontend code
- Accessibility audits and responsive testing

**Como acionar no Hermes:**
```text
/skill browser-qa
Execute esta tarefa usando esta skill e valide o resultado.
```

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
Execute esta tarefa usando esta skill e valide o resultado.
```

**Validação típica:**
- Resposta preserva conteúdo técnico essencial
- Código/comandos/erros estão exatos
- Idioma do usuário foi mantido
- Riscos críticos não foram comprimidos demais

---

### `codebase-onboarding`

**Arquivo:** [`.hermes/skills/curso-hermes/codebase-onboarding/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/codebase-onboarding/SKILL.md)

**O que faz:** Analyze an unfamiliar codebase and generate a structured onboarding guide with architecture map, key entry points, conventions, and a starter CLAUDE.md. Use when joining a new project or setting up Claude Code for the first time in a repo.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- First time opening a project with Claude Code
- Joining a new team or repository
- User asks "help me understand this codebase"
- User asks to generate a CLAUDE.md for a project
- User says "onboard me" or "walk me through this repo"

**Como acionar no Hermes:**
```text
/skill codebase-onboarding
Execute esta tarefa usando esta skill e valide o resultado.
```

---

### `database-migrations`

**Arquivo:** [`.hermes/skills/curso-hermes/database-migrations/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/database-migrations/SKILL.md)

**O que faz:** Database migration best practices for schema changes, data migrations, rollbacks, and zero-downtime deployments across PostgreSQL, MySQL, and common ORMs (Prisma, Drizzle, Kysely, Django, TypeORM, golang-migrate).

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Creating or altering database tables
- Adding/removing columns or indexes
- Running data migrations (backfill, transform)
- Planning zero-downtime schema changes
- Setting up migration tooling for a new project

**Como acionar no Hermes:**
```text
/skill database-migrations
Execute esta tarefa usando esta skill e valide o resultado.
```

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
Execute esta tarefa usando esta skill e valide o resultado.
```

**Validação típica:**
- Campos obrigatórios realmente precisam ser obrigatórios
- Índices cobrem filtros principais
- Constraints protegem integridade
- Migration tem rollback/plano de recuperação

---

### `deployment-patterns`

**Arquivo:** [`.hermes/skills/curso-hermes/deployment-patterns/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/deployment-patterns/SKILL.md)

**O que faz:** Deployment workflows, CI/CD pipeline patterns, Docker containerization, health checks, rollback strategies, and production readiness checklists for web applications.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Setting up CI/CD pipelines
- Dockerizing an application
- Planning deployment strategy (blue-green, canary, rolling)
- Implementing health checks and readiness probes
- Preparing for a production release

**Como acionar no Hermes:**
```text
/skill deployment-patterns
Containerize/publique esta aplicação e valide pós-deploy.
```

---

### `design-system`

**Arquivo:** [`.hermes/skills/curso-hermes/design-system/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/design-system/SKILL.md)

**O que faz:** Use this skill to generate or audit design systems, check visual consistency, and review PRs that touch styling.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Starting a new project that needs a design system
- Auditing an existing codebase for visual consistency
- Before a redesign — understand what you have
- When the UI looks "off" but you can't pinpoint why
- Reviewing PRs that touch styling

**Como acionar no Hermes:**
```text
/skill design-system
Execute esta tarefa usando esta skill e valide o resultado.
```

---

### `django-patterns`

**Arquivo:** [`.hermes/skills/curso-hermes/django-patterns/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/django-patterns/SKILL.md)

**O que faz:** Django architecture patterns, REST API design with DRF, ORM best practices, caching, signals, middleware, and production-grade Django apps.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Building Django web applications
- Designing Django REST Framework APIs
- Working with Django ORM and models
- Setting up Django project structure
- Implementing caching, signals, middleware

**Como acionar no Hermes:**
```text
/skill django-patterns
Execute esta tarefa usando esta skill e valide o resultado.
```

---

### `django-security`

**Arquivo:** [`.hermes/skills/curso-hermes/django-security/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/django-security/SKILL.md)

**O que faz:** Django security best practices, authentication, authorization, CSRF protection, SQL injection prevention, XSS prevention, and secure deployment configurations.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Setting up Django authentication and authorization
- Implementing user permissions and roles
- Configuring production security settings
- Reviewing Django application for security issues
- Deploying Django applications to production

**Como acionar no Hermes:**
```text
/skill django-security
Revise este projeto/API antes de publicar e liste achados acionáveis.
```

---

### `django-tdd`

**Arquivo:** [`.hermes/skills/curso-hermes/django-tdd/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/django-tdd/SKILL.md)

**O que faz:** Django testing strategies with pytest-django, TDD methodology, factory_boy, mocking, coverage, and testing Django REST Framework APIs.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Writing new Django applications
- Implementing Django REST Framework APIs
- Testing Django models, views, and serializers
- Setting up testing infrastructure for Django projects

**Como acionar no Hermes:**
```text
/skill django-tdd
Crie/rode testes para esta mudança e reporte evidência real.
```

---

### `django-verification`

**Arquivo:** [`.hermes/skills/curso-hermes/django-verification/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/django-verification/SKILL.md)

**O que faz:** Verification loop for Django projects: migrations, linting, tests with coverage, security scans, and deployment readiness checks before release or PR.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Before opening a pull request for a Django project
- After major model changes, migration updates, or dependency upgrades
- Pre-deployment verification for staging or production
- Running full environment → lint → test → security → deploy readiness pipeline
- Validating migration safety and test coverage

**Como acionar no Hermes:**
```text
/skill django-verification
Execute esta tarefa usando esta skill e valide o resultado.
```

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
Containerize/publique esta aplicação e valide pós-deploy.
```

**Validação típica:**
- Base image oficial e fixa por versão
- `WORKDIR` definido
- Dependências instaladas antes do copy completo para cache
- Build separado de runtime quando fizer sentido

---

### `docker-patterns`

**Arquivo:** [`.hermes/skills/curso-hermes/docker-patterns/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/docker-patterns/SKILL.md)

**O que faz:** Docker and Docker Compose patterns for local development, container security, networking, volume strategies, and multi-service orchestration.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Setting up Docker Compose for local development
- Designing multi-container architectures
- Troubleshooting container networking or volume issues
- Reviewing Dockerfiles for security and size
- Migrating from local dev to containerized workflow

**Como acionar no Hermes:**
```text
/skill docker-patterns
Containerize/publique esta aplicação e valide pós-deploy.
```

---

### `documentation-lookup`

**Arquivo:** [`.hermes/skills/curso-hermes/documentation-lookup/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/documentation-lookup/SKILL.md)

**O que faz:** Use up-to-date library and framework docs via Context7 MCP instead of training data. Activates for setup questions, API references, code examples, or when the user names a framework (e.g. React, Next.js, Prisma).

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Asks setup or configuration questions (e.g. "How do I configure Next.js middleware?")
- Requests code that depends on a library ("Write a Prisma query for...")
- Needs API or reference information ("What are the Supabase auth methods?")
- Mentions specific frameworks or libraries (React, Vue, Svelte, Express, Tailwind, Prisma, Supabase, etc.)

**Como acionar no Hermes:**
```text
/skill documentation-lookup
Execute esta tarefa usando esta skill e valide o resultado.
```

---

### `e2e-testing`

**Arquivo:** [`.hermes/skills/curso-hermes/e2e-testing/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/e2e-testing/SKILL.md)

**O que faz:** Playwright E2E testing patterns, Page Object Model, configuration, CI/CD integration, artifact management, and flaky test strategies.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Playwright E2E testing patterns, Page Object Model, configuration, CI/CD integration, artifact management, and flaky test strategies.

**Como acionar no Hermes:**
```text
/skill e2e-testing
Crie/rode testes para esta mudança e reporte evidência real.
```

---

### `error-handling`

**Arquivo:** [`.hermes/skills/curso-hermes/error-handling/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/error-handling/SKILL.md)

**O que faz:** Patterns for robust error handling across TypeScript, Python, and Go. Covers typed errors, error boundaries, retries, circuit breakers, and user-facing error messages.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Designing error types or exception hierarchies for a new module or service
- Adding retry logic or circuit breakers for unreliable external dependencies
- Reviewing API endpoints for missing error handling
- Implementing user-facing error messages and feedback
- Debugging cascading failures or silent error swallowing

**Como acionar no Hermes:**
```text
/skill error-handling
Execute esta tarefa usando esta skill e valide o resultado.
```

---

### `fastapi-patterns`

**Arquivo:** [`.hermes/skills/curso-hermes/fastapi-patterns/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/fastapi-patterns/SKILL.md)

**O que faz:** FastAPI best practices covering project structure, Pydantic v2 schemas, dependency injection, async handlers, authentication, authorization, transactional service layers, and testing with httpx and pytest.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- FastAPI best practices covering project structure, Pydantic v2 schemas, dependency injection, async handlers, authentication, authorization, transactional service layers, and testing with httpx and pytest.

**Como acionar no Hermes:**
```text
/skill fastapi-patterns
Implemente/revise esta API com validação, erros HTTP e testes.
```

---

### `frontend-a11y`

**Arquivo:** [`.hermes/skills/curso-hermes/frontend-a11y/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/frontend-a11y/SKILL.md)

**O que faz:** Accessibility patterns for React and Next.js — semantic HTML, ARIA attributes, form labeling, keyboard navigation, focus management, and screen reader support. Use when building any interactive UI component or form.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Building or reviewing form components (`<input>`, `<select>`, `<textarea>`)
- Creating interactive elements (modals, dropdowns, tooltips, tabs)
- Using `<div>` or `<span>` with `onClick`
- Adding `aria-*` attributes to any element
- Implementing keyboard navigation or focus management

**Como acionar no Hermes:**
```text
/skill frontend-a11y
Crie/revise esta tela e valide build, UX e erros de console.
```

**Validação típica:**
- Every `<input>`, `<select>`, and `<textarea>` has a connected `<label>` via `htmlFor`/`id`
- Error messages are linked with `aria-describedby` and marked `role="alert"`
- No `onClick` on `<div>` or `<span>` without `role`, `tabIndex`, and `onKeyDown`
- Icon-only buttons have `aria-label`

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
Crie/revise esta tela e valide build, UX e erros de console.
```

---

### `frontend-design-direction`

**Arquivo:** [`.hermes/skills/curso-hermes/frontend-design-direction/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/frontend-design-direction/SKILL.md)

**O que faz:** Set an ECC-specific frontend design direction for production UI work. Use when building or improving websites, dashboards, applications, components, landing pages, visual tools, or any web UI that needs stronger product-specific design judgment.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- The user asks to build a web page, app, dashboard, artifact, component, or UI.
- The user asks to make an interface more polished, distinctive, beautiful, or
- The implementation needs visual hierarchy, typography, color, motion, layout,
- The current UI works but reads as flat, generic, templated, or mismatched to

**Como acionar no Hermes:**
```text
/skill frontend-design-direction
Crie/revise esta tela e valide build, UX e erros de console.
```

---

### `frontend-patterns`

**Arquivo:** [`.hermes/skills/curso-hermes/frontend-patterns/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/frontend-patterns/SKILL.md)

**O que faz:** Frontend development patterns for React, Next.js, state management, performance optimization, and UI best practices.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Building React components (composition, props, rendering)
- Managing state (useState, useReducer, Zustand, Context)
- Implementing data fetching (SWR, React Query, server components)
- Optimizing performance (memoization, virtualization, code splitting)
- Working with forms (validation, controlled inputs, Zod schemas)

**Como acionar no Hermes:**
```text
/skill frontend-patterns
Crie/revise esta tela e valide build, UX e erros de console.
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
Crie/revise esta tela e valide build, UX e erros de console.
```

**Validação típica:**
- UI renderiza sem erro no console
- Fluxo principal funciona com mouse e teclado
- Mobile não quebra
- Build/lint/teste rodou ou bloqueio foi informado

---

### `git-workflow`

**Arquivo:** [`.hermes/skills/curso-hermes/git-workflow/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/git-workflow/SKILL.md)

**O que faz:** Git workflow patterns including branching strategies, commit conventions, merge vs rebase, conflict resolution, and collaborative development best practices for teams of all sizes.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Setting up Git workflow for a new project
- Deciding on branching strategy (GitFlow, trunk-based, GitHub flow)
- Writing commit messages and PR descriptions
- Resolving merge conflicts
- Managing releases and version tags

**Como acionar no Hermes:**
```text
/skill git-workflow
Execute esta tarefa usando esta skill e valide o resultado.
```

**Validação típica:**
- Code follows project style guidelines
- Self-review completed
- Comments added for complex logic
- Documentation updated

---

### `github-ops`

**Arquivo:** [`.hermes/skills/curso-hermes/github-ops/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/github-ops/SKILL.md)

**O que faz:** GitHub repository operations, automation, and management. Issue triage, PR management, CI/CD operations, release management, and security monitoring using the gh CLI. Use when the user wants to manage GitHub issues, PRs, CI status, releases, contributors, stale items, or any GitHub operational task beyond simple git commands.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Triaging issues (classifying, labeling, responding, deduplicating)
- Managing PRs (review status, CI checks, stale PRs, merge readiness)
- Debugging CI/CD failures
- Preparing releases and changelogs
- Monitoring Dependabot and security alerts

**Como acionar no Hermes:**
```text
/skill github-ops
Execute esta tarefa usando esta skill e valide o resultado.
```

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
Execute esta tarefa usando esta skill e valide o resultado.
```

---

### `hexagonal-architecture`

**Arquivo:** [`.hermes/skills/curso-hermes/hexagonal-architecture/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/hexagonal-architecture/SKILL.md)

**O que faz:** Design, implement, and refactor Ports & Adapters systems with clear domain boundaries, dependency inversion, and testable use-case orchestration across TypeScript, Java, Kotlin, and Go services.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Building new features where long-term maintainability and testability matter.
- Refactoring layered or framework-heavy code where domain logic is mixed with I/O concerns.
- Supporting multiple interfaces for the same use case (HTTP, CLI, queue workers, cron jobs).
- Replacing infrastructure (database, external APIs, message bus) without rewriting business rules.

**Como acionar no Hermes:**
```text
/skill hexagonal-architecture
Execute esta tarefa usando esta skill e valide o resultado.
```

---

### `laravel-patterns`

**Arquivo:** [`.hermes/skills/curso-hermes/laravel-patterns/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/laravel-patterns/SKILL.md)

**O que faz:** Laravel architecture patterns, routing/controllers, Eloquent ORM, service layers, queues, events, caching, and API resources for production apps.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Building Laravel web applications or APIs
- Structuring controllers, services, and domain logic
- Working with Eloquent models and relationships
- Designing APIs with resources and pagination
- Adding queues, events, caching, and background jobs

**Como acionar no Hermes:**
```text
/skill laravel-patterns
Execute esta tarefa usando esta skill e valide o resultado.
```

---

### `laravel-security`

**Arquivo:** [`.hermes/skills/curso-hermes/laravel-security/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/laravel-security/SKILL.md)

**O que faz:** Laravel security best practices — authentication, authorization, Eloquent safety, CSRF, XSS prevention, API security, and secure deployment configurations.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Setting up Laravel authentication and authorization (Sanctum, Passport, Jetstream, Breeze)
- Implementing user roles, permissions, and policies
- Configuring production security settings and environment variables
- Reviewing Laravel applications for security vulnerabilities
- Deploying Laravel applications to production

**Como acionar no Hermes:**
```text
/skill laravel-security
Revise este projeto/API antes de publicar e liste achados acionáveis.
```

---

### `laravel-tdd`

**Arquivo:** [`.hermes/skills/curso-hermes/laravel-tdd/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/laravel-tdd/SKILL.md)

**O que faz:** Laravel testing strategies with PHPUnit, Pest, model factories, HTTP tests, Sanctum authentication testing, mocking, and coverage.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Writing new Laravel applications or features
- Implementing API endpoints with Sanctum or Passport authentication
- Testing Eloquent models, relationships, scopes, and accessors
- Setting up testing infrastructure for Laravel projects
- Writing feature tests for HTTP controllers and form requests

**Como acionar no Hermes:**
```text
/skill laravel-tdd
Crie/rode testes para esta mudança e reporte evidência real.
```

---

### `laravel-verification`

**Arquivo:** [`.hermes/skills/curso-hermes/laravel-verification/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/laravel-verification/SKILL.md)

**O que faz:** Verification loop for Laravel projects: env checks, linting, static analysis, tests with coverage, security scans, and deployment readiness.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Before opening a pull request for a Laravel project
- After major refactors or dependency upgrades
- Pre-deployment verification for staging or production
- Running full lint -> test -> security -> deploy readiness pipeline

**Como acionar no Hermes:**
```text
/skill laravel-verification
Execute esta tarefa usando esta skill e valide o resultado.
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
Crie um MCP server/tool para esta integração e teste localmente.
```

**Validação típica:**
- Não expor segredo na resposta
- Não aceitar comando shell arbitrário
- Validar IDs/paths/URLs
- Rate limit/timeouts

---

### `mcp-server-patterns`

**Arquivo:** [`.hermes/skills/curso-hermes/mcp-server-patterns/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/mcp-server-patterns/SKILL.md)

**O que faz:** Build MCP servers with Node/TypeScript SDK — tools, resources, prompts, Zod validation, stdio vs Streamable HTTP. Use Context7 or official MCP docs for latest API.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Build MCP servers with Node/TypeScript SDK — tools, resources, prompts, Zod validation, stdio vs Streamable HTTP. Use Context7 or official MCP docs for latest API.

**Como acionar no Hermes:**
```text
/skill mcp-server-patterns
Crie um MCP server/tool para esta integração e teste localmente.
```

---

### `mysql-patterns`

**Arquivo:** [`.hermes/skills/curso-hermes/mysql-patterns/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/mysql-patterns/SKILL.md)

**O que faz:** MySQL and MariaDB schema, query, indexing, transaction, replication, and connection-pool patterns for production backends.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- MySQL and MariaDB schema, query, indexing, transaction, replication, and connection-pool patterns for production backends.

**Como acionar no Hermes:**
```text
/skill mysql-patterns
Execute esta tarefa usando esta skill e valide o resultado.
```

---

### `nestjs-patterns`

**Arquivo:** [`.hermes/skills/curso-hermes/nestjs-patterns/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/nestjs-patterns/SKILL.md)

**O que faz:** NestJS architecture patterns for modules, controllers, providers, DTO validation, guards, interceptors, config, and production-grade TypeScript backends.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Building NestJS APIs or services
- Structuring modules, controllers, and providers
- Adding DTO validation, guards, interceptors, or exception filters
- Configuring environment-aware settings and database integrations
- Testing NestJS units or HTTP endpoints

**Como acionar no Hermes:**
```text
/skill nestjs-patterns
Execute esta tarefa usando esta skill e valide o resultado.
```

---

### `nextjs-turbopack`

**Arquivo:** [`.hermes/skills/curso-hermes/nextjs-turbopack/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/nextjs-turbopack/SKILL.md)

**O que faz:** Next.js 16+ and Turbopack — incremental bundling, FS caching, dev speed, and when to use Turbopack vs webpack.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- **Turbopack (default dev)**: Use for day-to-day development. Faster cold start and HMR, especially in large apps.
- **Webpack (legacy dev)**: Use only if you hit a Turbopack bug or rely on a webpack-only plugin in dev. Disable with `--webpack` (or `--no-turbopack` depending on your Next.js version; check the docs for your release).
- **Production**: Production build behavior (`next build`) may use Turbopack or webpack depending on Next.js version; check the official Next.js docs for your version.

**Como acionar no Hermes:**
```text
/skill nextjs-turbopack
Execute esta tarefa usando esta skill e valide o resultado.
```

---

### `postgres-patterns`

**Arquivo:** [`.hermes/skills/curso-hermes/postgres-patterns/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/postgres-patterns/SKILL.md)

**O que faz:** PostgreSQL database patterns for query optimization, schema design, indexing, and security. Based on Supabase best practices.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Writing SQL queries or migrations
- Designing database schemas
- Troubleshooting slow queries
- Implementing Row Level Security
- Setting up connection pooling

**Como acionar no Hermes:**
```text
/skill postgres-patterns
Execute esta tarefa usando esta skill e valide o resultado.
```

---

### `prisma-patterns`

**Arquivo:** [`.hermes/skills/curso-hermes/prisma-patterns/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/prisma-patterns/SKILL.md)

**O que faz:** Prisma ORM patterns for TypeScript backends — schema design, query optimization, transactions, pagination, and critical traps like updateMany returning count not records, $transaction timeouts, migrate dev resetting the DB, @updatedAt skipped on bulk writes, and serverless connection exhaustion.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Designing or modifying Prisma schema models and relations
- Writing queries, transactions, or pagination logic
- Using `updateMany`, `deleteMany`, or any bulk operation
- Running or planning database migrations
- Deploying to serverless environments (Vercel, Lambda, Cloudflare Workers)

**Como acionar no Hermes:**
```text
/skill prisma-patterns
Execute esta tarefa usando esta skill e valide o resultado.
```

---

### `python-patterns`

**Arquivo:** [`.hermes/skills/curso-hermes/python-patterns/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/python-patterns/SKILL.md)

**O que faz:** Pythonic idioms, PEP 8 standards, type hints, and best practices for building robust, efficient, and maintainable Python applications.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Writing new Python code
- Reviewing Python code
- Refactoring existing Python code
- Designing Python packages/modules

**Como acionar no Hermes:**
```text
/skill python-patterns
Execute esta tarefa usando esta skill e valide o resultado.
```

---

### `python-testing`

**Arquivo:** [`.hermes/skills/curso-hermes/python-testing/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/python-testing/SKILL.md)

**O que faz:** Python testing strategies using pytest, TDD methodology, fixtures, mocking, parametrization, and coverage requirements.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Writing new Python code (follow TDD: red, green, refactor)
- Designing test suites for Python projects
- Reviewing Python test coverage
- Setting up testing infrastructure

**Como acionar no Hermes:**
```text
/skill python-testing
Crie/rode testes para esta mudança e reporte evidência real.
```

---

### `react-patterns`

**Arquivo:** [`.hermes/skills/curso-hermes/react-patterns/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/react-patterns/SKILL.md)

**O que faz:** React 18/19 patterns including hooks discipline, server/client component boundaries, Suspense + error boundaries, form actions, data fetching, state management decision trees, and accessibility-first composition. Use when writing or reviewing React components.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Writing or modifying React function components, custom hooks, or component trees
- Reviewing JSX/TSX files
- Designing state shape or component composition
- Migrating class components or older `forwardRef`/`useEffect`-heavy code
- Choosing between local state, lifted state, context, and external stores

**Como acionar no Hermes:**
```text
/skill react-patterns
Crie/revise esta tela e valide build, UX e erros de console.
```

---

### `react-performance`

**Arquivo:** [`.hermes/skills/curso-hermes/react-performance/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/react-performance/SKILL.md)

**O que faz:** React and Next.js performance optimization patterns adapted from Vercel Engineering's React Best Practices (https://github.com/vercel-labs/agent-skills). Organizes 70+ rules across 8 priority categories — waterfalls, bundle size, server-side, client fetching, re-render, rendering, JS micro-perf, advanced. Use when writing, reviewing, or refactoring React/Next.js code for performance.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Writing or reviewing React/Next.js code for performance
- Diagnosing slow page loads, slow interactions, or high CPU on the client
- Auditing bundle size or Lighthouse Core Web Vitals regressions
- Removing waterfalls in Server Components / API routes
- Reducing client-side re-renders

**Como acionar no Hermes:**
```text
/skill react-performance
Crie/revise esta tela e valide build, UX e erros de console.
```

---

### `react-testing`

**Arquivo:** [`.hermes/skills/curso-hermes/react-testing/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/react-testing/SKILL.md)

**O que faz:** React component testing with React Testing Library, Vitest/Jest, MSW for network mocking, accessibility assertions with axe, and the decision boundary between component tests and Playwright/Cypress end-to-end runs. Use when writing or fixing tests for React components, hooks, or pages.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Writing tests for React components, custom hooks, or pages
- Adding test coverage to legacy untested components
- Migrating from Enzyme or class-component-era patterns to React Testing Library
- Setting up Vitest or Jest for a new React project
- Mocking HTTP requests in tests

**Como acionar no Hermes:**
```text
/skill react-testing
Crie/revise esta tela e valide build, UX e erros de console.
```

---

### `security-review`

**Arquivo:** [`.hermes/skills/curso-hermes/security-review/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/security-review/SKILL.md)

**O que faz:** Use this skill when adding authentication, handling user input, working with secrets, creating API endpoints, or implementing payment/sensitive features. Provides comprehensive security checklist and patterns.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Implementing authentication or authorization
- Handling user input or file uploads
- Creating new API endpoints
- Working with secrets or credentials
- Implementing payment features

**Como acionar no Hermes:**
```text
/skill security-review
Revise este projeto/API antes de publicar e liste achados acionáveis.
```

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
Revise este projeto/API antes de publicar e liste achados acionáveis.
```

**Validação típica:**
- Nenhum token/senha hardcoded
- `.env` fora do git
- Logs não imprimem segredo
- Chaves de produção não usadas localmente sem necessidade

---

### `tdd-workflow`

**Arquivo:** [`.hermes/skills/curso-hermes/tdd-workflow/SKILL.md`](https://github.com/clfigueiredo/hermes-infra-skills/blob/main/.hermes/skills/curso-hermes/tdd-workflow/SKILL.md)

**O que faz:** Use this skill when writing new features, fixing bugs, or refactoring code. Enforces test-driven development with 80%+ coverage including unit, integration, and E2E tests.

**Tags:** `curso-hermes`, `operational`, `ecc`

**Quando usar:**
- Writing new features or functionality
- Fixing bugs or issues
- Refactoring existing code
- Adding API endpoints
- Creating new components

**Como acionar no Hermes:**
```text
/skill tdd-workflow
Crie/rode testes para esta mudança e reporte evidência real.
```

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
Crie/rode testes para esta mudança e reporte evidência real.
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
Execute esta tarefa usando esta skill e valide o resultado.
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
Execute esta tarefa usando esta skill e valide o resultado.
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
Execute esta tarefa usando esta skill e valide o resultado.
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
Execute esta tarefa usando esta skill e valide o resultado.
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
Execute esta tarefa usando esta skill e valide o resultado.
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
Execute esta tarefa usando esta skill e valide o resultado.
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
Containerize/publique esta aplicação e valide pós-deploy.
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
Execute esta tarefa usando esta skill e valide o resultado.
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
Execute esta tarefa usando esta skill e valide o resultado.
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
Execute esta tarefa usando esta skill e valide o resultado.
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
Execute esta tarefa usando esta skill e valide o resultado.
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
Execute esta tarefa usando esta skill e valide o resultado.
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
Execute esta tarefa usando esta skill e valide o resultado.
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
Execute esta tarefa usando esta skill e valide o resultado.
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
Execute esta tarefa usando esta skill e valide o resultado.
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
Execute esta tarefa usando esta skill e valide o resultado.
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
Execute esta tarefa usando esta skill e valide o resultado.
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
Execute esta tarefa usando esta skill e valide o resultado.
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
Execute esta tarefa usando esta skill e valide o resultado.
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
Execute esta tarefa usando esta skill e valide o resultado.
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
Execute esta tarefa usando esta skill e valide o resultado.
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
Execute esta tarefa usando esta skill e valide o resultado.
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
Execute esta tarefa usando esta skill e valide o resultado.
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
Execute esta tarefa usando esta skill e valide o resultado.
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
Execute esta tarefa usando esta skill e valide o resultado.
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
Execute esta tarefa usando esta skill e valide o resultado.
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
Execute esta tarefa usando esta skill e valide o resultado.
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
Execute esta tarefa usando esta skill e valide o resultado.
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
Execute esta tarefa usando esta skill e valide o resultado.
```

---

## Manutenção deste catálogo

Sempre que adicionar/remover skills, regenere esta página lendo todos os `SKILL.md`.
