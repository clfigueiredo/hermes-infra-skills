---
name: frontend-react-nextjs
description: >
  Use quando o aluno estiver criando ou revisando frontend React/Next.js. Cobre componentes, estado, forms, acessibilidade, performance, responsividade, UX e build sem transformar o projeto em arquitetura exagerada.
version: 1.0.0
author: Fórum Telecom / Hermes Course, adapted from affaan-m/ecc
license: MIT
metadata:
  hermes:
    tags: [curso-hermes, frontend, react, nextjs, ui, accessibility]
    related_skills: [frontend-browser-qa, testing-quality-gates, security-review-webapp]
    source: https://github.com/affaan-m/ecc
---

# Frontend React/Next.js

## Quando usar

- Criar tela, landing page, dashboard ou componente
- Corrigir build/erro de React/Next
- Melhorar responsividade/performance
- Revisar acessibilidade
- Organizar estado/forms

## Checklist de implementação

1. **Componente pequeno** — uma responsabilidade por componente.
2. **Props claras** — tipos explícitos; nada de `any` sem motivo.
3. **Estado certo** — local para UI simples; TanStack/Zustand/Context só quando necessário.
4. **Dados** — loading, erro, vazio e sucesso sempre tratados.
5. **Forms** — validação no cliente e no servidor.
6. **Acessibilidade** — label, foco, teclado, contraste, semantic HTML.
7. **Performance** — evitar objeto/função inline pesada; memoizar só quando há ganho.
8. **Responsivo** — mobile primeiro.
9. **Build** — rodar `npm run build`/`pnpm build` quando possível.

## Padrão de correção de bug

```text
Causa: <motivo técnico>
Fix: <mudança exata>
Validação: <build/teste/fluxo de UI>
```

## Armadilhas comuns

- Criar componente gigante com 500 linhas.
- Usar `useEffect` para tudo.
- Duplicar estado derivado.
- Esquecer estado de erro/loading.
- Quebrar acessibilidade com `div` clicável sem botão.
- Otimizar antes de medir.

## Verificação

- [ ] UI renderiza sem erro no console
- [ ] Fluxo principal funciona com mouse e teclado
- [ ] Mobile não quebra
- [ ] Build/lint/teste rodou ou bloqueio foi informado
## Atribuição

Adaptado e sintetizado a partir de padrões do projeto MIT `affaan-m/ecc`:

- Fonte: https://github.com/affaan-m/ecc
- Licença original: MIT

Esta versão foi reduzida, traduzida e ajustada para uso operacional no Hermes Agent, sem hooks/instaladores externos.
