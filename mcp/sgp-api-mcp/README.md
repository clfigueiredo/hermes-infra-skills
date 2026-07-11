# SGP API MCP Server

MCP server para integrar Hermes Agent/Claude/Codex com a API do SGP Provedor a partir da documentação Postman oficial informada no curso.

Documentação analisada:

- https://documenter.getpostman.com/view/6682240/2sB34hHg2V

## O que ele expõe

- Catálogo consultável dos 237 endpoints da coleção Postman.
- Chamada genérica controlada `sgp_request`.
- Tools prontas para fluxos comuns:
  - pré-cadastro: planos, vencimentos, vendedores;
  - cliente/contratos/faturas;
  - ordens de serviço e anotações;
  - FTTH: OLTs, ONUs e info de ONU;
  - RADIUS/PPPoE: status de login;
  - Gerenciador CPE: detalhes do serviço/CPE.

## Segurança

Por padrão:

- `SGP_READ_ONLY=true` bloqueia endpoints perigosos/escrita;
- `SGP_MASK_SENSITIVE=true` mascara CPF/CNPJ, telefone, e-mail, senha, token, login e endereço;
- timeout configurável;
- token/senha só via ambiente, nunca no prompt.

## Instalação

```bash
cd mcp/sgp-api-mcp
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Configure `.env` ou variáveis do serviço:

```bash
export SGP_BASE_URL="https://seudominio.sgp.net.br"
export SGP_USERNAME="usuario_sgp"     # se usar Basic Auth
export SGP_PASSWORD="senha_sgp"
export SGP_APP="nome_app"             # se usar app/token
export SGP_TOKEN="token_sgp"
export SGP_READ_ONLY="true"
export SGP_MASK_SENSITIVE="true"
export SGP_TIMEOUT="20"
```

## Rodar localmente

```bash
source .venv/bin/activate
python server.py
```

## Configurar no Hermes

Exemplo conceitual usando MCP stdio:

```bash
hermes mcp add sgp-api --command "bash -lc 'cd /CAMINHO/hermes-infra-skills/mcp/sgp-api-mcp && source .venv/bin/activate && python server.py'"
hermes mcp test sgp-api
```

Depois use no Hermes:

```text
Liste as tools do MCP sgp-api e consulte o catálogo de endpoints de FTTH.
```

## Tools principais

- `sgp_config_status()`
- `sgp_api_catalog(category, search, include_dangerous, limit)`
- `sgp_request(method, path, params, body, auth_mode, allow_write)`
- `sgp_precadastro_planos()`
- `sgp_precadastro_vencimentos()`
- `sgp_precadastro_vendedores()`
- `sgp_cliente_consultar(cpfcnpj, contrato, nome, login, onu_serial)`
- `sgp_cliente_contratos(cpfcnpj)`
- `sgp_titulos_listar(cpfcnpj, contrato, cliente_id, limit)`
- `sgp_os_listar(filtros)`
- `sgp_os_anotacoes(os_id)`
- `sgp_ftth_olts()`
- `sgp_ftth_onus(olt_id)`
- `sgp_ftth_onu_info(id_onu)`
- `sgp_radius_status(login, contrato)`
- `sgp_cpe_detalhes(id_servico)`

## Observação importante

A coleção SGP mistura autenticações: Basic Auth, token/app e credenciais da Central do Assinante. O MCP tenta ser flexível, mas a configuração real do ambiente do provedor prevalece. Em produção, teste primeiro endpoint read-only com usuário/token limitado.
