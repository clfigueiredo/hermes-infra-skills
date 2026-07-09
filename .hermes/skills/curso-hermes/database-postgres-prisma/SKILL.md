---
name: database-postgres-prisma
description: >
  Use quando o aluno estiver modelando banco, criando migrations, usando PostgreSQL/MySQL/Prisma ou investigando lentidão/erro de query. Foca em schema simples, índices, transações, paginação e migração segura.
version: 1.0.0
author: Fórum Telecom / Hermes Course, adapted from affaan-m/ecc
license: MIT
metadata:
  hermes:
    tags: [curso-hermes, database, postgres, mysql, prisma, migrations]
    related_skills: [backend-api-patterns, security-review-webapp]
    source: https://github.com/affaan-m/ecc
---

# Database Postgres/Prisma

## Quando usar

- Criar schema/tabelas
- Escrever migration
- Corrigir query lenta
- Usar Prisma/ORM
- Definir relacionamento e índices

## Regras

1. Modelar pelos casos de uso reais.
2. Usar chave primária estável.
3. Criar índices para filtros/joins frequentes.
4. Evitar N+1.
5. Usar transação para mudanças multi-tabela.
6. Nunca concatenar SQL com input do usuário.
7. Migration destrutiva exige backup/plano de rollback.

## Migration segura

```text
1. Backup/restore validado
2. Migration aditiva primeiro
3. Backfill se necessário
4. Deploy da aplicação compatível
5. Remoção de coluna/código antigo só depois
```

## Checklist

- [ ] Campos obrigatórios realmente precisam ser obrigatórios
- [ ] Índices cobrem filtros principais
- [ ] Constraints protegem integridade
- [ ] Migration tem rollback/plano de recuperação
- [ ] Query crítica foi explicada/medida quando possível
- [ ] Dados sensíveis não ficam em log
## Atribuição

Adaptado e sintetizado a partir de padrões do projeto MIT `affaan-m/ecc`:

- Fonte: https://github.com/affaan-m/ecc
- Licença original: MIT

Esta versão foi reduzida, traduzida e ajustada para uso didático no Hermes Agent, sem hooks/instaladores externos.
