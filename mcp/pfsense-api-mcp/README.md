# pfSense API MCP Server

MCP server read-first para integrar Hermes Agent/Claude/Codex com pfSense CE/Plus usando o pacote REST API/pfrest quando disponível.

## Segurança

- `PFSENSE_READ_ONLY=true` por padrão.
- Bloqueia métodos não-GET e endpoints com termos perigosos sem `allow_write=true`.
- Mascara campos sensíveis em respostas.
- Não salva nem imprime senha/token.

## Instalação

```bash
cd mcp/pfsense-api-mcp
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
cp .env.example .env
# edite .env localmente
python server.py
```

## Tools

- `pfsense_config_status`
- `pfsense_endpoint_catalog`
- `pfsense_request`
- `pfsense_system_status`
- `pfsense_firewall_rules`
- `pfsense_firewall_aliases`
- `pfsense_dhcp_leases`

## Observação

pfSense não tem API universal em todas as versões/instalações. Este MCP assume o pacote REST API/pfrest ou compatível. Em ambientes sem API, use a skill `pfsense-ops` para diagnóstico via SSH/WebGUI read-only.
