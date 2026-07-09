---
name: vibe-coding-starter
description: >
  Use quando o aluno quiser transformar uma ideia vaga em um sistema funcional com Hermes Agent. Define fluxo de vibe coding seguro: intenção, escopo, arquitetura mínima, fatias verticais, implementação, teste, revisão e validação real antes de declarar pronto.
version: 1.0.0
author: Fórum Telecom / Hermes Course, adapted from affaan-m/ecc
license: MIT
metadata:
  hermes:
    tags: [curso-hermes, vibe-coding, planning, mvp, software-development]
    related_skills: [frontend-react-nextjs, backend-api-patterns, security-review-webapp, testing-quality-gates]
    source: https://github.com/affaan-m/ecc
---

# Vibe Coding Starter

## Visão geral

Use esta skill para guiar o aluno do pedido solto até um MVP validado. O objetivo não é só "gerar código", mas fazer o Hermes trabalhar como engenheiro: entender intenção, dividir escopo, implementar em fatias pequenas e validar com execução real.

## Quando usar

- "Cria um SaaS/app/site/sistema pra mim"
- "Tenho uma ideia, me ajuda a fazer"
- "Faz um MVP"
- "Transforma esse briefing em projeto"
- Aluno está usando IA para programar sem método

Não use para uma correção pequena já localizada; nesse caso use uma skill específica.

## Fluxo obrigatório

1. **Intenção** — descreva o resultado em 3 linhas: usuário, problema, resultado esperado.
2. **Escopo mínimo** — liste o que entra no MVP e o que fica fora.
3. **Stack** — confirme linguagem/framework/banco/deploy. Se não houver, escolha padrão simples.
4. **Fatias verticais** — quebre em entregas testáveis: tela + API + banco + validação.
5. **Contrato** — defina rotas, modelos, estados e critérios de aceite.
6. **Implementação** — altere poucos arquivos por vez.
7. **Validação** — rode build/teste/lint/app sempre que possível.
8. **Revisão** — procure bugs, segurança, performance e UX.
9. **Resumo final** — diga o que foi feito, comandos rodados e pendências reais.

## Padrão de resposta inicial

```text
Objetivo: <sistema em 1 frase>
Usuários: <quem usa>
MVP inclui:
- ...
Fora do MVP:
- ...
Primeira fatia:
- ...
Validação:
- ...
```

## Regras de execução

- Não criar projeto gigante sem fatias.
- Não declarar pronto sem rodar validação.
- Não inventar output de teste.
- Não usar dependência pesada sem motivo.
- Preferir funcional simples antes de visual complexo.
- Se houver autenticação/pagamento/dados sensíveis, carregar revisão de segurança.

## Critérios de pronto

- [ ] MVP tem escopo claro
- [ ] Cada fatia tem critério de aceite
- [ ] Código executou ou bloqueio foi declarado
- [ ] Erros reais foram corrigidos ou registrados
- [ ] Próximo passo está claro para o aluno
## Atribuição

Adaptado e sintetizado a partir de padrões do projeto MIT `affaan-m/ecc`:

- Fonte: https://github.com/affaan-m/ecc
- Licença original: MIT

Esta versão foi reduzida, traduzida e ajustada para uso didático no Hermes Agent, sem hooks/instaladores externos.
