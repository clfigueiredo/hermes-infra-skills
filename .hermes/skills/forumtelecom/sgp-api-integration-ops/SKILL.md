---
name: sgp-api-integration-ops
description: "Use when integrating Hermes Agent with SGP Provedor/SGP Sistemas API for ISP operations: safe API credential handling, endpoint discovery, read-only customer/contract/financial lookups, plan/pre-registration endpoints, ticket/workflow automation, WhatsApp attendant integration, Python/curl clients, logging, validation, and production safety controls."
version: 1.0.0
author: Hermes Agent / Forum Telecom
license: MIT
metadata:
  hermes:
    tags: [sgp, sgp-provedor, isp, erp, api, integracao, atendimento, financeiro, contratos, python]
    related_skills: [atendimento-isp-n1-n2, financeiro-ops, tr069-acs-ops, zabbix-ops]
    source_research:
      - https://github.com/ltitelecom/sgp-form-assinatura
      - https://documenter.getpostman.com/view/6682240/2sB34hHg2V
    mcp_server: mcp/sgp-api-mcp
    html_reference: docs/sgp-api-capabilities.html
---
# SGP Provedor — Integração API com Hermes

Skill para criar integrações seguras entre Hermes Agent e SGP Provedor/SGP Sistemas em ambientes de ISP/MSP. O foco é consultar dados operacionais por API, apoiar atendimento via WhatsApp, automatizar rotinas repetitivas e preparar scripts que não exponham tokens.

## Contrato operacional

Use esta skill quando o usuário pedir:
- integrar Hermes com SGP;
- consultar cliente, contrato, plano, financeiro ou status por API;
- criar atendimento N1/N2 que consulte ERP antes de diagnosticar rede;
- criar pré-cadastro/assinatura usando endpoint do SGP;
- listar planos, vendedores ou vencimentos de pré-cadastro;
- abrir chamado/OS ou registrar observação, se a API do ambiente permitir;
- montar cliente Python/curl seguro para testes de API.

Não invente endpoint sensível se a documentação do ambiente não foi enviada. Quando a documentação não estiver pública, faça primeiro uma etapa de descoberta controlada com o operador.

## Segurança obrigatória

1. **Nunca pedir ou colar token no grupo**: token deve ir em `.env`, cofre local, variáveis do sistema ou DM seguro.
2. **Read-only por padrão**: começar com consultas; cadastro, alteração financeira, bloqueio/desbloqueio ou abertura de OS exige autorização explícita.
3. **Permissões mínimas**: gerar token/app no SGP com escopo mínimo e, se possível, somente leitura para laboratório.
4. **Mascarar PII**: CPF/CNPJ, telefone, endereço, e-mail, login PPPoE e dados financeiros devem sair mascarados no grupo.
5. **Não logar token**: logs devem registrar URL/endpoint/status/latência, nunca `token`, `Authorization` ou payload sensível completo.
6. **Ambiente de teste primeiro**: validar em conta/cliente fake antes de apontar para produção.
7. **Timeout e rate limit**: toda chamada precisa de timeout e tratamento de erro para não travar atendimento.

## Documentação oficial analisada e artefatos gerados

A documentação Postman enviada no curso foi analisada e mapeada em 237 endpoints:

```text
https://documenter.getpostman.com/view/6682240/2sB34hHg2V
```

Artefatos no repositório:

- MCP server: `mcp/sgp-api-mcp`
- Catálogo JSON: `mcp/sgp-api-mcp/sgp_api_catalog.json`
- Análise Markdown: `mcp/sgp-api-mcp/SGP-API-ANALYSIS.md`
- HTML objetivo: `docs/sgp-api-capabilities.html`

Categorias mapeadas:

```text
Central Assinante, CRM, Estoque, FTTH, Gerenciador CPE,
Ordem de Serviço, Pré-Cadastro, RADIUS, Remessa/Retorno,
Suporte, Termo de Aceite, URA e Outros.
```

O MCP expõe tools read-only por padrão para catálogo, cliente, contratos, títulos, OS, FTTH, RADIUS, CPE e pré-cadastro. Operações perigosas/escrita ficam bloqueadas por `SGP_READ_ONLY=true`.

## Credenciais e variáveis de ambiente

Referência pública de integração com SGP usa:

- `URL_SGP`: URL base, exemplo `https://seudominio.sgp.net.br`;
- `APP_SGP`: nome do app criado no SGP;
- `TOKEN_SGP`: token gerado no SGP em **Administração > Integrações > Tokens**.

No Hermes, preferir `.env`:

```bash
SGP_BASE_URL="https://seudominio.sgp.net.br"
SGP_APP="nome-do-app"
SGP_TOKEN="token-no-cofre"
SGP_TIMEOUT="20"
SGP_READ_ONLY="true"
```

Nunca publicar o valor real de `SGP_TOKEN`.

## Endpoints observados em referência pública

A referência pública `ltitelecom/sgp-form-assinatura` mostra endpoints de pré-cadastro:

```text
POST /api/precadastro/plano/list
POST /api/precadastro/vencimento/list
POST /api/precadastro/vendedor/list
POST /api/precadastro/F
POST /api/precadastro/J
```

Payload básico observado:

```json
{
  "app": "APP_SGP",
  "token": "TOKEN_SGP"
}
```

Header observado:

```text
Content-Type: application/json
Authorization: *** <TOKEN_SGP>
```

Atenção: a API instalada no SGP do aluno pode ter endpoints adicionais ou formato diferente. A documentação do ambiente prevalece sobre estes exemplos.

## Teste mínimo de conectividade

Com `curl`, sem expor token no terminal compartilhado:

```bash
set -a
source .env
set +a

curl -sS -m "${SGP_TIMEOUT:-20}" \
  -X POST "${SGP_BASE_URL%/}/api/precadastro/plano/list" \
  -H 'Content-Type: application/json' \
  -H "Authorization: *** ${SGP_TOKEN}" \
  --data "{\"app\":\"${SGP_APP}\",\"token\":\"${SGP_TOKEN}\"}" \
  | python3 -m json.tool
```

Se retornar HTML/login, provável endpoint errado, bloqueio por ACL, token inválido ou URL base incorreta.

## Cliente Python seguro

Crie `sgp_client.py`:

```python
import os
import json
import requests

class SGPClient:
    def __init__(self, base_url=None, app=None, token=None, timeout=None):
        self.base_url = (base_url or os.environ["SGP_BASE_URL"]).rstrip("/")
        self.app = app or os.environ["SGP_APP"]
        self.token = token or os.environ["SGP_TOKEN"]
        self.timeout = int(timeout or os.getenv("SGP_TIMEOUT", "20"))

    def post(self, path, payload=None):
        body = {"app": self.app, "token": self.token}
        if payload:
            body.update(payload)
        url = f"{self.base_url}/{path.lstrip('/')}"
        r = requests.post(
            url,
            json=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"*** {self.token}",
            },
            timeout=self.timeout,
        )
        r.raise_for_status()
        try:
            return r.json()
        except ValueError:
            return {"raw": r.text[:1000]}

    def listar_planos_precadastro(self):
        return self.post("/api/precadastro/plano/list")

    def listar_vencimentos_precadastro(self):
        return self.post("/api/precadastro/vencimento/list")

    def listar_vendedores_precadastro(self):
        return self.post("/api/precadastro/vendedor/list")

if __name__ == "__main__":
    c = SGPClient()
    data = c.listar_planos_precadastro()
    print(json.dumps(data, ensure_ascii=False, indent=2))
```

Execução:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install requests
python sgp_client.py
```

## Descoberta controlada de documentação/endpoints

Quando o aluno fornecer documentação ou URL do Swagger/Postman:

1. baixar a documentação com ferramenta de arquivo/web;
2. identificar autenticação real: body, header, bearer, basic, token/app;
3. separar endpoints em leitura e escrita;
4. criar uma tabela local de capacidades;
5. testar primeiro endpoint read-only simples;
6. mascarar dados antes de responder no grupo.

Checklist de endpoints úteis para ISP:

```text
Cliente:
- buscar por CPF/CNPJ, telefone, contrato, login PPPoE ou ID
- retornar nome mascarado, contrato, status e plano

Financeiro:
- títulos em aberto
- status de inadimplência
- vencimento
- segunda via/link, se permitido

Técnico:
- contrato/login PPPoE
- plano/velocidade
- endereço ou coordenada
- CTO/OLT/porta/ONU se o SGP armazenar

Atendimento:
- abrir chamado/OS
- anexar observação
- consultar chamados abertos

Pré-cadastro:
- listar planos
- listar vencimentos
- listar vendedores
- enviar pré-cadastro PF/PJ
```

## Fluxo para atendimento WhatsApp com Hermes

```text
Cliente chama no WhatsApp
  -> Hermes identifica telefone/origem
  -> Consulta SGP por telefone/CPF/contrato/login
  -> Confirma cliente com dado mascarado
  -> Checa financeiro e contrato
  -> Se financeiro ok, segue diagnóstico técnico
  -> Consulta Zabbix/OLT/RADIUS/BNG conforme skill relacionada
  -> Responde ou abre chamado/OS no SGP
```

Prompt operacional:

```text
/skill sgp-api-integration-ops
Integre o Hermes com o SGP usando somente leitura primeiro. Use as variáveis SGP_BASE_URL, SGP_APP e SGP_TOKEN do .env. Valide conectividade, liste endpoints disponíveis na documentação que vou enviar e crie funções Python seguras para consulta de cliente, financeiro e contrato sem expor PII.
```

## Exemplo de wrapper para consulta com máscara

```python
def mask_doc(value: str) -> str:
    digits = ''.join(ch for ch in str(value) if ch.isdigit())
    if len(digits) <= 4:
        return "***"
    return digits[:3] + "***" + digits[-2:]

def mask_phone(value: str) -> str:
    digits = ''.join(ch for ch in str(value) if ch.isdigit())
    if len(digits) < 8:
        return "***"
    return digits[:2] + "*****" + digits[-4:]

def safe_customer_summary(c):
    return {
        "id": c.get("id"),
        "nome": (c.get("nome") or "")[:2] + "***",
        "documento": mask_doc(c.get("cpfcnpj", "")),
        "telefone": mask_phone(c.get("telefone", "")),
        "status": c.get("status"),
        "plano": c.get("plano"),
    }
```

## Esqueleto FastAPI para expor ferramenta interna ao Hermes

Use quando quiser evitar que o Hermes conheça detalhes brutos da API do SGP. A API interna recebe pedidos de alto nível e aplica máscara, RBAC e logs.

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Hermes SGP Gateway")

class ClienteQuery(BaseModel):
    telefone: str | None = None
    contrato: str | None = None
    login: str | None = None

@app.post("/cliente/buscar")
def buscar_cliente(q: ClienteQuery):
    # chamar SGPClient aqui
    # retornar apenas campos mascarados/necessários
    return {"ok": True, "cliente": None}
```

## Tratamento de erros

```python
try:
    data = client.post('/api/precadastro/plano/list')
except requests.Timeout:
    return 'SGP não respondeu dentro do timeout.'
except requests.HTTPError as e:
    code = e.response.status_code if e.response is not None else 'sem-status'
    return f'Erro HTTP no SGP: {code}. Verificar URL, token/app e ACL.'
except requests.RequestException as e:
    return 'Falha de rede até o SGP. Validar DNS, firewall, VPN e certificado TLS.'
```

## Validação antes de produção

- [ ] Token criado em `Administração > Integrações > Tokens` ou local equivalente.
- [ ] Token com menor privilégio possível.
- [ ] `.env` configurado e fora do Git.
- [ ] Conectividade validada com endpoint read-only.
- [ ] Dados sensíveis mascarados no retorno.
- [ ] Timeout configurado.
- [ ] Logs sem token/payload sensível.
- [ ] Operações de escrita bloqueadas por `SGP_READ_ONLY=true` até autorização.
- [ ] Testado com cliente fake/laboratório.

## Armadilhas comuns

1. **Confundir assinatura ChatGPT/API com integração SGP**: são coisas separadas; token do SGP vem do painel do SGP.
2. **Colar token no grupo**: revogar e gerar outro imediatamente.
3. **Assumir endpoint padrão**: SGP pode variar por versão/módulo; confirmar na documentação do cliente.
4. **Automatizar bloqueio/desbloqueio cedo demais**: comece por consulta e abertura de chamado.
5. **Responder com CPF/endereço completo**: sempre mascarar.
6. **Sem timeout**: atendimento trava quando ERP fica lento.
7. **Sem rate limit**: bot em loop pode sobrecarregar ERP.
8. **Ignorar status financeiro**: antes de diagnosticar rede, checar inadimplência quando política do provedor permitir.

## Comandos úteis de diagnóstico

```bash
# DNS/TLS
python3 - <<'PY'
import os, socket, urllib.parse
u=urllib.parse.urlparse(os.environ['SGP_BASE_URL'])
print(socket.gethostbyname(u.hostname))
PY

# HTTP status sem token
curl -I -m 10 "$SGP_BASE_URL"

# Teste de endpoint com token via env, sem imprimir token
python3 - <<'PY'
import os, requests
url=os.environ['SGP_BASE_URL'].rstrip('/') + '/api/precadastro/plano/list'
r=requests.post(url, json={'app': os.environ['SGP_APP'], 'token': os.environ['SGP_TOKEN']}, timeout=20)
print(r.status_code, r.headers.get('content-type'))
print(r.text[:300])
PY
```
