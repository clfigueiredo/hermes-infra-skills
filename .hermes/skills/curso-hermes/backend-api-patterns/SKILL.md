---
name: backend-api-patterns
description: >
  Use quando o aluno estiver criando ou revisando backend/API. Cobre rotas REST, camada service/repository, validação, erros HTTP, autenticação, rate limit, paginação, logs e contrato entre frontend/backend.
version: 1.0.0
author: Fórum Telecom / Hermes Course, adapted from affaan-m/ecc
license: MIT
metadata:
  hermes:
    tags: [curso-hermes, backend, api, rest, node, fastapi, django, laravel]
    related_skills: [database-postgres-prisma, security-review-webapp, testing-quality-gates]
    source: https://github.com/affaan-m/ecc
---

# Backend/API Patterns

## Quando usar

- Criar endpoint REST/GraphQL
- Organizar controller/service/repository
- Validar input
- Corrigir erro HTTP/API
- Integrar frontend com backend

## Padrões mínimos

### Rotas REST

```text
GET    /resources
GET    /resources/:id
POST   /resources
PATCH  /resources/:id
DELETE /resources/:id
```

Use query params para filtro/paginação:

```text
GET /customers?status=active&page=1&pageSize=20
```

### Camadas

- **Controller/route:** HTTP, auth, validação, status code.
- **Service/use-case:** regra de negócio.
- **Repository/DAO:** banco/API externa.
- **Schema/DTO:** contrato de entrada/saída.

### Erros HTTP

| Caso | Status |
|---|---:|
| Não autenticado | 401 |
| Sem permissão | 403 |
| Não encontrado | 404 |
| Validação | 400 ou 422 |
| Conflito | 409 |
| Rate limit | 429 |
| Erro interno | 500 |

## Checklist

- [ ] Input validado por schema
- [ ] Erros não vazam stack/segredo
- [ ] Auth/permission checada no servidor
- [ ] Paginação em listas
- [ ] Logs têm request id/correlação
- [ ] Teste cobre sucesso + erro
- [ ] Frontend sabe contrato de resposta
## Atribuição

Adaptado e sintetizado a partir de padrões do projeto MIT `affaan-m/ecc`:

- Fonte: https://github.com/affaan-m/ecc
- Licença original: MIT

Esta versão foi reduzida, traduzida e ajustada para uso operacional no Hermes Agent, sem hooks/instaladores externos.
