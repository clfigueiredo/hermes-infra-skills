---
name: security-review-webapp
description: >
  Use quando o aluno criar autenticação, API, upload, pagamento, painel admin, integração externa ou qualquer código com dados sensíveis. Aplica checklist prático de segurança web antes de publicar.
version: 1.0.0
author: Fórum Telecom / Hermes Course, adapted from affaan-m/ecc
license: MIT
metadata:
  hermes:
    tags: [curso-hermes, security, webapp, auth, secrets, owasp]
    related_skills: [backend-api-patterns, frontend-react-nextjs, testing-quality-gates]
    source: https://github.com/affaan-m/ecc
---

# Security Review Webapp

## Quando usar

- Login/autenticação/autorização
- API nova
- Upload de arquivo
- Dados pessoais/sensíveis
- Pagamento/webhook
- Admin dashboard
- Deploy público

## Checklist essencial

### Segredos

- [ ] Nenhum token/senha hardcoded
- [ ] `.env` fora do git
- [ ] Logs não imprimem segredo
- [ ] Chaves de produção não usadas localmente sem necessidade

### Input

- [ ] Todo input validado por schema
- [ ] SQL/ORM usa query parametrizada
- [ ] Upload tem limite de tamanho/tipo/extensão
- [ ] Erro não vaza stack trace

### Auth/Authz

- [ ] Endpoint privado exige autenticação
- [ ] Permissão checada no servidor
- [ ] `userId` vem da sessão/token, não do body
- [ ] Sessão/token expira
- [ ] Admin separado de usuário comum

### Web

- [ ] CSRF considerado para cookie/session
- [ ] XSS evitado: sem HTML bruto inseguro
- [ ] CORS restrito
- [ ] Rate limit em login/API sensível
- [ ] Webhook valida assinatura

## Formato de achado

```text
Arquivo:linha: severidade: problema.
Impacto: o que atacante consegue.
Correção: mudança concreta.
Teste: como provar que fechou.
```

## Severidade

| Nível | Significado |
|---|---|
| Crítico | invasão, vazamento, dinheiro, admin |
| Alto | bypass auth, leitura indevida, execução perigosa |
| Médio | abuso limitado, enumeração, falta de rate limit |
| Baixo | hardening, mensagem, cabeçalho |

## Regra

Nunca responda "seguro" sem evidência. Diga o que foi verificado e o que não foi.
## Atribuição

Adaptado e sintetizado a partir de padrões do projeto MIT `affaan-m/ecc`:

- Fonte: https://github.com/affaan-m/ecc
- Licença original: MIT

Esta versão foi reduzida, traduzida e ajustada para uso didático no Hermes Agent, sem hooks/instaladores externos.
