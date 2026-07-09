---
name: testing-quality-gates
description: >
  Use quando o aluno implementar feature/correção e precisar provar que funciona. Define gates de qualidade: teste mínimo, build, lint, E2E quando aplicável, regressão e evidência real de execução.
version: 1.0.0
author: Fórum Telecom / Hermes Course, adapted from affaan-m/ecc
license: MIT
metadata:
  hermes:
    tags: [curso-hermes, testing, tdd, quality, build, regression]
    related_skills: [vibe-coding-starter, frontend-browser-qa, security-review-webapp]
    source: https://github.com/affaan-m/ecc
---

# Testing Quality Gates

## Quando usar

- Depois de alterar código
- Ao corrigir bug
- Antes de entregar MVP
- Quando o aluno diz "acho que funcionou"

## Gates mínimos

1. **Reprodução** — para bug, primeiro provar o erro.
2. **Teste** — unitário/integrado/E2E conforme risco.
3. **Build** — projeto compila.
4. **Lint/typecheck** — quando existir.
5. **Fluxo manual** — para UI, testar no navegador.
6. **Regressão** — confirmar que o caso antigo não voltou.

## Matriz rápida

| Mudança | Gate mínimo |
|---|---|
| Componente UI | teste visual/manual + console limpo |
| API | teste sucesso + erro + auth |
| Banco | migration + teste rollback/plano |
| Segurança | teste que falha antes e passa depois |
| Refactor | suíte existente verde |

## Relatório final

```text
Validação executada:
- <comando>: <resultado>
- <fluxo manual>: <resultado>
Não validado:
- <motivo real>
```

## Proibido

- Inventar saída de teste.
- Dizer "deve funcionar" como se fosse validação.
- Ignorar erro de build não relacionado sem avisar.
## Atribuição

Adaptado e sintetizado a partir de padrões do projeto MIT `affaan-m/ecc`:

- Fonte: https://github.com/affaan-m/ecc
- Licença original: MIT

Esta versão foi reduzida, traduzida e ajustada para uso didático no Hermes Agent, sem hooks/instaladores externos.
