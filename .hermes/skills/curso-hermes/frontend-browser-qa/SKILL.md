---
name: frontend-browser-qa
description: >
  Use quando o aluno precisar validar visualmente uma aplicação web. Define fluxo de QA com navegador: abrir app, testar caminho feliz, estados de erro/vazio, responsividade, console, network e acessibilidade básica.
version: 1.0.0
author: Fórum Telecom / Hermes Course, adapted from affaan-m/ecc
license: MIT
metadata:
  hermes:
    tags: [curso-hermes, browser-qa, e2e, playwright, frontend, validation]
    related_skills: [frontend-react-nextjs, testing-quality-gates]
    source: https://github.com/affaan-m/ecc
---

# Frontend Browser QA

## Quando usar

- Depois de criar/alterar tela
- Antes de dizer "está funcionando"
- Para validar fluxo de login/cadastro/checkout/dashboard
- Quando o aluno diz "ficou bugado" ou manda print

## Fluxo

1. Subir app local se necessário.
2. Abrir URL no navegador.
3. Testar caminho feliz.
4. Testar campos inválidos/vazios.
5. Testar responsividade: desktop e mobile.
6. Checar console JS.
7. Checar requests com erro.
8. Registrar bug com passo de reprodução.
9. Corrigir e repetir o fluxo afetado.

## Relato de bug

```text
Bug: <descrição curta>
Reprodução:
1. ...
2. ...
Esperado: ...
Atual: ...
Evidência: console/network/screenshot
Fix sugerido: ...
```

## Critérios mínimos

- [ ] Página carrega
- [ ] Fluxo principal conclui
- [ ] Erros aparecem de forma compreensível
- [ ] Console sem erro novo
- [ ] Layout não quebra em mobile
- [ ] Ação crítica tem feedback visual
## Atribuição

Adaptado e sintetizado a partir de padrões do projeto MIT `affaan-m/ecc`:

- Fonte: https://github.com/affaan-m/ecc
- Licença original: MIT

Esta versão foi reduzida, traduzida e ajustada para uso operacional no Hermes Agent, sem hooks/instaladores externos.
