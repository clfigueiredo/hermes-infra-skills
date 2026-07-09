# Skills Curso Hermes

Skills **operacionais** para alunos do Hermes Agent: vibe coding, desenvolvimento, revisão, segurança, testes, deploy, GitHub, MCP e agentes convertidos do ECC.

## Instalação

```bash
mkdir -p ~/.hermes/skills
cp -a .hermes/skills/curso-hermes ~/.hermes/skills/
```

Depois, dentro do Hermes:

```text
/reload-skills
```

## Skills disponíveis

| Skill | Uso |
|---|---|
| `accessibility` | Design, implement, and audit inclusive digital products using WCAG 2.2 Level AA standards. Use this skill to generate semantic ARIA for Web and accessibility traits for Web and Native platforms (iOS/Android). |
| `agent-build-error-resolver` | Use quando o aluno precisar do comportamento operacional do agente ECC `build-error-resolver`. Build and TypeScript error resolution specialist. Use PROACTIVELY when build fails or type errors occur. Fixes build/type errors only with minimal diffs, no architectural edits. Focuses on getting the build green quickly. |
| `agent-code-architect` | Use quando o aluno precisar do comportamento operacional do agente ECC `code-architect`. Designs feature architectures by analyzing existing codebase patterns and conventions, then providing implementation blueprints with concrete files, interfaces, data flow, and build order. |
| `agent-code-explorer` | Use quando o aluno precisar do comportamento operacional do agente ECC `code-explorer`. Deeply analyzes existing codebase features by tracing execution paths, mapping architecture layers, and documenting dependencies to inform new development. |
| `agent-code-reviewer` | Use quando o aluno precisar do comportamento operacional do agente ECC `code-reviewer`. Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code. MUST BE USED for all code changes. |
| `agent-code-simplifier` | Use quando o aluno precisar do comportamento operacional do agente ECC `code-simplifier`. Simplifies and refines code for clarity, consistency, and maintainability while preserving behavior. Focus on recently modified code unless instructed otherwise. |
| `agent-database-reviewer` | Use quando o aluno precisar do comportamento operacional do agente ECC `database-reviewer`. PostgreSQL database specialist for query optimization, schema design, security, and performance. Use PROACTIVELY when writing SQL, creating migrations, designing schemas, or troubleshooting database performance. Incorporates Supabase best practices. |
| `agent-docs-lookup` | Use quando o aluno precisar do comportamento operacional do agente ECC `docs-lookup`. When the user asks how to use a library, framework, or API or needs up-to-date code examples, use Context7 MCP to fetch current documentation and return answers with examples. Invoke for docs/API/setup questions. |
| `agent-e2e-runner` | Use quando o aluno precisar do comportamento operacional do agente ECC `e2e-runner`. End-to-end testing specialist using Vercel Agent Browser (preferred) with Playwright fallback. Use PROACTIVELY for generating, maintaining, and running E2E tests. Manages test journeys, quarantines flaky tests, uploads artifacts (screenshots, videos, traces), and ensures critical user flows work. |
| `agent-fastapi-reviewer` | Use quando o aluno precisar do comportamento operacional do agente ECC `fastapi-reviewer`. Reviews FastAPI applications for async correctness, dependency injection, Pydantic schemas, security, OpenAPI quality, testing, and production readiness. |
| `agent-performance-optimizer` | Use quando o aluno precisar do comportamento operacional do agente ECC `performance-optimizer`. Performance analysis and optimization specialist. Use PROACTIVELY for identifying bottlenecks, optimizing slow code, reducing bundle sizes, and improving runtime performance. Profiling, memory leaks, render optimization, and algorithmic improvements. |
| `agent-planner` | Use quando o aluno precisar do comportamento operacional do agente ECC `planner`. Expert planning specialist for complex features and refactoring. Use PROACTIVELY when users request feature implementation, architectural changes, or complex refactoring. Automatically activated for planning tasks. |
| `agent-pr-test-analyzer` | Use quando o aluno precisar do comportamento operacional do agente ECC `pr-test-analyzer`. Review pull request test coverage quality and completeness, with emphasis on behavioral coverage and real bug prevention. |
| `agent-python-reviewer` | Use quando o aluno precisar do comportamento operacional do agente ECC `python-reviewer`. Expert Python code reviewer specializing in PEP 8 compliance, Pythonic idioms, type hints, security, and performance. Use for all Python code changes. MUST BE USED for Python projects. |
| `agent-react-build-resolver` | Use quando o aluno precisar do comportamento operacional do agente ECC `react-build-resolver`. Diagnose and fix React build failures across Vite, webpack, Next.js, CRA, Parcel, esbuild, and Bun. Handles JSX/TSX compile errors, hydration mismatches, server/client component boundary failures, missing types, and bundler-specific configuration issues with minimal, surgical changes. MUST BE USED when a React build fails. |
| `agent-react-reviewer` | Use quando o aluno precisar do comportamento operacional do agente ECC `react-reviewer`. Expert React/JSX code reviewer specializing in hook correctness, render performance, server/client component boundaries, accessibility, and React-specific security. Use for any change touching .tsx/.jsx files or React component logic. MUST BE USED for React projects. |
| `agent-security-reviewer` | Use quando o aluno precisar do comportamento operacional do agente ECC `security-reviewer`. Security vulnerability detection and remediation specialist. Use PROACTIVELY after writing code that handles user input, authentication, API endpoints, or sensitive data. Flags secrets, SSRF, injection, unsafe crypto, and OWASP Top 10 vulnerabilities. |
| `agent-tdd-guide` | Use quando o aluno precisar do comportamento operacional do agente ECC `tdd-guide`. Test-Driven Development specialist enforcing write-tests-first methodology. Use PROACTIVELY when writing new features, fixing bugs, or refactoring code. Ensures 80%+ test coverage. |
| `agent-typescript-reviewer` | Use quando o aluno precisar do comportamento operacional do agente ECC `typescript-reviewer`. Expert TypeScript/JavaScript code reviewer specializing in type safety, async correctness, Node/web security, and idiomatic patterns. Use for all TypeScript and JavaScript code changes. MUST BE USED for TypeScript/JavaScript projects. |
| `ai-regression-testing` | Regression testing strategies for AI-assisted development. Sandbox-mode API testing without database dependencies, automated bug-check workflows, and patterns to catch AI blind spots where the same model writes and reviews code. |
| `api-design` | REST API design patterns including resource naming, status codes, pagination, filtering, error responses, versioning, and rate limiting for production APIs. |
| `backend-api-patterns` | Use quando o aluno estiver criando ou revisando backend/API. Cobre rotas REST, camada service/repository, validação, erros HTTP, autenticação, rate limit, paginação, logs e contrato entre frontend/backend. |
| `backend-patterns` | Backend architecture patterns, API design, database optimization, and server-side best practices for Node.js, Express, and Next.js API routes. |
| `browser-qa` | Use this skill to automate visual testing and UI interaction verification using browser automation after deploying features. |
| `caveman-terse-mode` | Use quando o aluno quiser reduzir tokens/verbosidade do Hermes Agent sem perder conteúdo técnico. Ativa um modo de resposta ultra objetivo em PT-BR ou no idioma do usuário, preservando comandos, código, erros, nomes de APIs e avisos críticos. Inclui padrões para resposta curta, mensagens de commit, revisão de código e compressão segura de textos de memória/instruções. |
| `codebase-onboarding` | Analyze an unfamiliar codebase and generate a structured onboarding guide with architecture map, key entry points, conventions, and a starter CLAUDE.md. Use when joining a new project or setting up Claude Code for the first time in a repo. |
| `database-migrations` | Database migration best practices for schema changes, data migrations, rollbacks, and zero-downtime deployments across PostgreSQL, MySQL, and common ORMs (Prisma, Drizzle, Kysely, Django, TypeORM, golang-migrate). |
| `database-postgres-prisma` | Use quando o aluno estiver modelando banco, criando migrations, usando PostgreSQL/MySQL/Prisma ou investigando lentidão/erro de query. Foca em schema simples, índices, transações, paginação e migração segura. |
| `deployment-patterns` | Deployment workflows, CI/CD pipeline patterns, Docker containerization, health checks, rollback strategies, and production readiness checklists for web applications. |
| `design-system` | Use this skill to generate or audit design systems, check visual consistency, and review PRs that touch styling. |
| `django-patterns` | Django architecture patterns, REST API design with DRF, ORM best practices, caching, signals, middleware, and production-grade Django apps. |
| `django-security` | Django security best practices, authentication, authorization, CSRF protection, SQL injection prevention, XSS prevention, and secure deployment configurations. |
| `django-tdd` | Django testing strategies with pytest-django, TDD methodology, factory_boy, mocking, coverage, and testing Django REST Framework APIs. |
| `django-verification` | Verification loop for Django projects: migrations, linting, tests with coverage, security scans, and deployment readiness checks before release or PR. |
| `docker-deploy-basics` | Use quando o aluno quiser containerizar ou publicar uma aplicação. Cobre Dockerfile simples, Compose, variáveis de ambiente, healthcheck, logs, rollback básico e validação pós-deploy. |
| `docker-patterns` | Docker and Docker Compose patterns for local development, container security, networking, volume strategies, and multi-service orchestration. |
| `documentation-lookup` | Use up-to-date library and framework docs via Context7 MCP instead of training data. Activates for setup questions, API references, code examples, or when the user names a framework (e.g. React, Next.js, Prisma). |
| `e2e-testing` | Playwright E2E testing patterns, Page Object Model, configuration, CI/CD integration, artifact management, and flaky test strategies. |
| `error-handling` | Patterns for robust error handling across TypeScript, Python, and Go. Covers typed errors, error boundaries, retries, circuit breakers, and user-facing error messages. |
| `fastapi-patterns` | FastAPI best practices covering project structure, Pydantic v2 schemas, dependency injection, async handlers, authentication, authorization, transactional service layers, and testing with httpx and pytest. |
| `frontend-a11y` | Accessibility patterns for React and Next.js — semantic HTML, ARIA attributes, form labeling, keyboard navigation, focus management, and screen reader support. Use when building any interactive UI component or form. |
| `frontend-browser-qa` | Use quando o aluno precisar validar visualmente uma aplicação web. Define fluxo de QA com navegador: abrir app, testar caminho feliz, estados de erro/vazio, responsividade, console, network e acessibilidade básica. |
| `frontend-design-direction` | Set an ECC-specific frontend design direction for production UI work. Use when building or improving websites, dashboards, applications, components, landing pages, visual tools, or any web UI that needs stronger product-specific design judgment. |
| `frontend-patterns` | Frontend development patterns for React, Next.js, state management, performance optimization, and UI best practices. |
| `frontend-react-nextjs` | Use quando o aluno estiver criando ou revisando frontend React/Next.js. Cobre componentes, estado, forms, acessibilidade, performance, responsividade, UX e build sem transformar o projeto em arquitetura exagerada. |
| `git-workflow` | Git workflow patterns including branching strategies, commit conventions, merge vs rebase, conflict resolution, and collaborative development best practices for teams of all sizes. |
| `github-ops` | GitHub repository operations, automation, and management. Issue triage, PR management, CI/CD operations, release management, and security monitoring using the gh CLI. Use when the user wants to manage GitHub issues, PRs, CI status, releases, contributors, stale items, or any GitHub operational task beyond simple git commands. |
| `github-workflow-student` | Use quando o aluno trabalhar com GitHub: criar repo, commits, branches, pull requests, issues, releases e CI básico. Foca em fluxo seguro e simples para projetos de estudo e MVPs. |
| `hexagonal-architecture` | Design, implement, and refactor Ports & Adapters systems with clear domain boundaries, dependency inversion, and testable use-case orchestration across TypeScript, Java, Kotlin, and Go services. |
| `laravel-patterns` | Laravel architecture patterns, routing/controllers, Eloquent ORM, service layers, queues, events, caching, and API resources for production apps. |
| `laravel-security` | Laravel security best practices — authentication, authorization, Eloquent safety, CSRF, XSS prevention, API security, and secure deployment configurations. |
| `laravel-tdd` | Laravel testing strategies with PHPUnit, Pest, model factories, HTTP tests, Sanctum authentication testing, mocking, and coverage. |
| `laravel-verification` | Verification loop for Laravel projects: env checks, linting, static analysis, tests with coverage, security scans, and deployment readiness. |
| `mcp-server-builder` | Use quando o aluno quiser criar um MCP server para Hermes/agents. Orienta design de tools, schemas, validação, stdio/HTTP, segurança, testes locais e documentação mínima. |
| `mcp-server-patterns` | Build MCP servers with Node/TypeScript SDK — tools, resources, prompts, Zod validation, stdio vs Streamable HTTP. Use Context7 or official MCP docs for latest API. |
| `mysql-patterns` | MySQL and MariaDB schema, query, indexing, transaction, replication, and connection-pool patterns for production backends. |
| `nestjs-patterns` | NestJS architecture patterns for modules, controllers, providers, DTO validation, guards, interceptors, config, and production-grade TypeScript backends. |
| `nextjs-turbopack` | Next.js 16+ and Turbopack — incremental bundling, FS caching, dev speed, and when to use Turbopack vs webpack. |
| `postgres-patterns` | PostgreSQL database patterns for query optimization, schema design, indexing, and security. Based on Supabase best practices. |
| `prisma-patterns` | Prisma ORM patterns for TypeScript backends — schema design, query optimization, transactions, pagination, and critical traps like updateMany returning count not records, $transaction timeouts, migrate dev resetting the DB, @updatedAt skipped on bulk writes, and serverless connection exhaustion. |
| `python-patterns` | Pythonic idioms, PEP 8 standards, type hints, and best practices for building robust, efficient, and maintainable Python applications. |
| `python-testing` | Python testing strategies using pytest, TDD methodology, fixtures, mocking, parametrization, and coverage requirements. |
| `react-patterns` | React 18/19 patterns including hooks discipline, server/client component boundaries, Suspense + error boundaries, form actions, data fetching, state management decision trees, and accessibility-first composition. Use when writing or reviewing React components. |
| `react-performance` | React and Next.js performance optimization patterns adapted from Vercel Engineering's React Best Practices (https://github.com/vercel-labs/agent-skills). Organizes 70+ rules across 8 priority categories — waterfalls, bundle size, server-side, client fetching, re-render, rendering, JS micro-perf, advanced. Use when writing, reviewing, or refactoring React/Next.js code for performance. |
| `react-testing` | React component testing with React Testing Library, Vitest/Jest, MSW for network mocking, accessibility assertions with axe, and the decision boundary between component tests and Playwright/Cypress end-to-end runs. Use when writing or fixing tests for React components, hooks, or pages. |
| `security-review` | Use this skill when adding authentication, handling user input, working with secrets, creating API endpoints, or implementing payment/sensitive features. Provides comprehensive security checklist and patterns. |
| `security-review-webapp` | Use quando o aluno criar autenticação, API, upload, pagamento, painel admin, integração externa ou qualquer código com dados sensíveis. Aplica checklist prático de segurança web antes de publicar. |
| `tdd-workflow` | Use this skill when writing new features, fixing bugs, or refactoring code. Enforces test-driven development with 80%+ coverage including unit, integration, and E2E tests. |
| `testing-quality-gates` | Use quando o aluno implementar feature/correção e precisar provar que funciona. Define gates de qualidade: teste mínimo, build, lint, E2E quando aplicável, regressão e evidência real de execução. |
| `vibe-coding-starter` | Use quando o aluno quiser transformar uma ideia vaga em um sistema funcional com Hermes Agent. Define fluxo de vibe coding seguro: intenção, escopo, arquitetura mínima, fatias verticais, implementação, teste, revisão e validação real antes de declarar pronto. |

## Organização

Esta pasta é separada de `forumtelecom/`.

- `curso-hermes/`: skills operacionais gerais dos alunos.
- `forumtelecom/`: skills de operação de infraestrutura/telecom.

## Fontes

Skills adaptadas/sintetizadas de projetos MIT públicos, com atribuição em cada `SKILL.md`:

- https://github.com/affaan-m/ecc
- https://github.com/JuliusBrussee/caveman
