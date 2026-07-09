# Skills Curso Hermes

Skills gerais para alunos do Hermes Agent: vibe coding, desenvolvimento, revisão, segurança, produtividade e operação do próprio agente.

## Instalação

A partir da raiz deste repositório:

```bash
mkdir -p ~/.hermes/skills
cp -a .hermes/skills/curso-hermes ~/.hermes/skills/
```

Depois, dentro do Hermes:

```text
/reload-skills
```

Ou reinicie a sessão/gateway.

## Skills disponíveis

| Skill | Uso |
|---|---|
| `vibe-coding-starter` | transformar ideia vaga em MVP validado |
| `frontend-react-nextjs` | frontend React/Next.js, UI, estado, performance |
| `frontend-browser-qa` | validação visual/browser/E2E básica |
| `backend-api-patterns` | APIs, services, repositories, erros HTTP |
| `database-postgres-prisma` | schema, migrations, queries, ORM |
| `security-review-webapp` | revisão de segurança web/app/API |
| `testing-quality-gates` | testes, build, lint, regressão, evidência |
| `docker-deploy-basics` | Docker, Compose e deploy simples |
| `github-workflow-student` | GitHub, branches, commits, PRs e CI básico |
| `mcp-server-builder` | criação de MCP servers/tools para Hermes |
| `caveman-terse-mode` | respostas curtas, economia de tokens, commits/reviews objetivos |

## Organização

Esta pasta é separada de `forumtelecom/`.

- `curso-hermes/`: skills didáticas gerais dos alunos.
- `forumtelecom/`: skills de operação de infraestrutura/telecom.

## Fontes

Algumas skills foram adaptadas/sintetizadas de projetos MIT públicos, com atribuição no próprio `SKILL.md`:

- https://github.com/affaan-m/ecc
- https://github.com/JuliusBrussee/caveman
