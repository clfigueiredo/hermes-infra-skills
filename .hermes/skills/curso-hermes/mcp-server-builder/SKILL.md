---
name: mcp-server-builder
description: >
  Use quando o aluno quiser criar um MCP server para Hermes/agents. Orienta design de tools, schemas, validação, stdio/HTTP, segurança, testes locais e documentação mínima.
version: 1.0.0
author: Fórum Telecom / Hermes Course, adapted from affaan-m/ecc
license: MIT
metadata:
  hermes:
    tags: [curso-hermes, mcp, tools, integrations, hermes-agent]
    related_skills: [backend-api-patterns, security-review-webapp, testing-quality-gates]
    source: https://github.com/affaan-m/ecc
---

# MCP Server Builder

## Quando usar

- Criar integração externa para Hermes
- Expor API interna como ferramenta
- Criar tool para banco, CRM, NOC, arquivos ou automação
- Ensinar aluno a conectar sistemas ao agente

## Design de tool

Cada tool precisa:

- nome curto e claro;
- descrição com quando usar e quando não usar;
- schema de entrada estrito;
- validação de parâmetros;
- saída JSON previsível;
- erros claros;
- limites de segurança.

## Checklist de segurança

- [ ] Não expor segredo na resposta
- [ ] Não aceitar comando shell arbitrário
- [ ] Validar IDs/paths/URLs
- [ ] Rate limit/timeouts
- [ ] Logs sem token/senha
- [ ] Permissões mínimas

## Fluxo de criação

1. Definir caso de uso.
2. Listar tools mínimas.
3. Escrever schemas.
4. Implementar com timeout/erro claro.
5. Testar cada tool isolada.
6. Conectar no Hermes.
7. Documentar instalação e exemplos.

## Critério de pronto

- [ ] MCP inicia localmente
- [ ] Hermes consegue listar tools
- [ ] Tool principal retorna JSON válido
- [ ] Falhas são tratadas sem stack/secreto
- [ ] README tem comando de instalação/teste
## Atribuição

Adaptado e sintetizado a partir de padrões do projeto MIT `affaan-m/ecc`:

- Fonte: https://github.com/affaan-m/ecc
- Licença original: MIT

Esta versão foi reduzida, traduzida e ajustada para uso operacional no Hermes Agent, sem hooks/instaladores externos.
