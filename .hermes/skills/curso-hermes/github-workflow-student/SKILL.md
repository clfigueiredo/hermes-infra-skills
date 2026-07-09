---
name: github-workflow-student
description: >
  Use quando o aluno trabalhar com GitHub: criar repo, commits, branches, pull requests, issues, releases e CI básico. Foca em fluxo seguro e simples para projetos de estudo e MVPs.
version: 1.0.0
author: Fórum Telecom / Hermes Course, adapted from affaan-m/ecc
license: MIT
metadata:
  hermes:
    tags: [curso-hermes, github, git, pull-request, ci]
    related_skills: [caveman-terse-mode, testing-quality-gates]
    source: https://github.com/affaan-m/ecc
---

# GitHub Workflow Student

## Quando usar

- Criar/clonar repo
- Organizar branch
- Gerar commit message
- Abrir PR
- Revisar diff
- Configurar CI simples

## Fluxo simples

```bash
git status
git checkout -b feat/minha-feature
git add .
git commit -m "feat: add minha feature"
git push -u origin feat/minha-feature
```

Depois abrir PR no GitHub ou via `gh pr create` se `gh` estiver autenticado.

## Antes do commit

- [ ] `git diff` revisado
- [ ] Sem segredo em arquivo
- [ ] Build/teste rodou quando possível
- [ ] Commit message curta e clara

## PR bom

```text
## O que mudou
- ...

## Como testar
- ...

## Evidência
- comando/print/log
```

## Erros comuns

- Commitar `.env`.
- Commit gigante sem tema único.
- Misturar refactor com feature.
- Fazer force push em branch compartilhada sem avisar.
## Atribuição

Adaptado e sintetizado a partir de padrões do projeto MIT `affaan-m/ecc`:

- Fonte: https://github.com/affaan-m/ecc
- Licença original: MIT

Esta versão foi reduzida, traduzida e ajustada para uso operacional no Hermes Agent, sem hooks/instaladores externos.
