---
name: docker-deploy-basics
description: >
  Use quando o aluno quiser containerizar ou publicar uma aplicação. Cobre Dockerfile simples, Compose, variáveis de ambiente, healthcheck, logs, rollback básico e validação pós-deploy.
version: 1.0.0
author: Fórum Telecom / Hermes Course, adapted from affaan-m/ecc
license: MIT
metadata:
  hermes:
    tags: [curso-hermes, docker, compose, deploy, devops]
    related_skills: [backend-api-patterns, testing-quality-gates, security-review-webapp]
    source: https://github.com/affaan-m/ecc
---

# Docker Deploy Basics

## Quando usar

- Criar Dockerfile
- Criar docker-compose
- Subir app com banco/cache
- Debugar container que não inicia
- Preparar deploy simples

## Checklist Dockerfile

- [ ] Base image oficial e fixa por versão
- [ ] `WORKDIR` definido
- [ ] Dependências instaladas antes do copy completo para cache
- [ ] Build separado de runtime quando fizer sentido
- [ ] App roda como usuário não-root quando possível
- [ ] Porta documentada
- [ ] Variáveis por env, não hardcoded

## Checklist Compose

- [ ] Serviços nomeados claramente
- [ ] Volumes para dados persistentes
- [ ] Network padrão suficiente, sem expor DB à internet
- [ ] Healthcheck quando possível
- [ ] `.env` não versionado com segredo real

## Debug rápido

```bash
docker compose ps
docker compose logs -f <service>
docker compose exec <service> sh
docker inspect <container>
```

## Validação pós-deploy

- [ ] Container `healthy` ou rodando
- [ ] Endpoint HTTP responde
- [ ] Logs sem erro repetindo
- [ ] Banco conectado
- [ ] Restart mantém dados persistentes
## Atribuição

Adaptado e sintetizado a partir de padrões do projeto MIT `affaan-m/ecc`:

- Fonte: https://github.com/affaan-m/ecc
- Licença original: MIT

Esta versão foi reduzida, traduzida e ajustada para uso didático no Hermes Agent, sem hooks/instaladores externos.
