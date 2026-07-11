#!/usr/bin/env python3
"""MCP server para SGP Provedor API.

Configuração via ambiente:
  SGP_BASE_URL=https://seusgp.exemplo.com.br
  SGP_USERNAME=usuario_sgp          # para Basic Auth, quando usado
  SGP_PASSWORD=senha_sgp
  SGP_APP=nome_app                  # para autenticação por app/token
  SGP_TOKEN=token_sgp
  SGP_TIMEOUT=20
  SGP_READ_ONLY=true                # bloqueia escrita/perigo por padrão
  SGP_MASK_SENSITIVE=true           # mascara PII/segredos na resposta
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("sgp-api-mcp")
CATALOG = json.loads((Path(__file__).with_name("sgp_api_catalog.json")).read_text(encoding="utf-8"))

DANGEROUS_RE = re.compile(
    r"(criar|cadastrar|alterar|atualizar|delete|deletar|remover|reset|reboot|autorizar|deauth|pagamento|pix|upload|anexo|add|edit|update|disconnect|desconectar|aceitar|promessa|libera|estorno|transfer|vincular|senha)",
    re.I,
)
SENSITIVE_KEY_RE = re.compile(r"(token|senha|password|secret|cpf|cnpj|cpfcnpj|documento|telefone|celular|email|endereco|logradouro|cep|login)", re.I)


def env_bool(name: str, default: bool = False) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return v.strip().lower() in {"1", "true", "yes", "sim", "on"}


def config() -> Dict[str, Any]:
    return {
        "base_url": os.getenv("SGP_BASE_URL", "").rstrip("/"),
        "username": os.getenv("SGP_USERNAME"),
        "password": os.getenv("SGP_PASSWORD"),
        "app": os.getenv("SGP_APP"),
        "token": os.getenv("SGP_TOKEN"),
        "timeout": int(os.getenv("SGP_TIMEOUT", "20")),
        "read_only": env_bool("SGP_READ_ONLY", True),
        "mask_sensitive": env_bool("SGP_MASK_SENSITIVE", True),
    }


def require_base_url() -> str:
    base = config()["base_url"]
    if not base:
        raise ValueError("SGP_BASE_URL não configurado")
    return base


def mask_value(value: Any) -> Any:
    if value is None:
        return value
    s = str(value)
    digits = "".join(ch for ch in s if ch.isdigit())
    if len(digits) >= 8:
        return digits[:3] + "***" + digits[-2:]
    if len(s) > 6:
        return s[:2] + "***" + s[-2:]
    return "***"


def mask_sensitive(obj: Any) -> Any:
    if not config()["mask_sensitive"]:
        return obj
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            out[k] = mask_value(v) if SENSITIVE_KEY_RE.search(str(k)) else mask_sensitive(v)
        return out
    if isinstance(obj, list):
        return [mask_sensitive(x) for x in obj]
    return obj


def is_dangerous(method: str, path: str, name: str = "") -> bool:
    text = f"{method} {path} {name}"
    if DANGEROUS_RE.search(text):
        return True
    # POST pode ser leitura no SGP, então não bloquear só por método.
    if method.upper() in {"PUT", "PATCH", "DELETE"}:
        return True
    return False


def prepare_body(body: Optional[Dict[str, Any]], include_app_token: bool = True) -> Dict[str, Any]:
    cfg = config()
    out = dict(body or {})
    if include_app_token:
        if cfg["app"] and "app" not in out:
            out["app"] = cfg["app"]
        if cfg["token"] and "token" not in out:
            out["token"] = cfg["token"]
    return out


def request_sgp(method: str, path: str, *, params: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None,
                auth_mode: str = "auto", allow_write: bool = False, include_app_token: bool = True,
                name: str = "") -> Dict[str, Any]:
    cfg = config()
    method = method.upper()
    path = path.replace("{{url}}", "").strip()
    if not path.startswith("/"):
        path = "/" + path
    if cfg["read_only"] and not allow_write and is_dangerous(method, path, name):
        return {"ok": False, "blocked": True, "reason": "SGP_READ_ONLY=true bloqueou endpoint de escrita/perigoso", "method": method, "path": path}

    url = require_base_url() + path
    headers = {"Accept": "application/json"}
    auth = None
    payload = prepare_body(body, include_app_token=include_app_token)

    if auth_mode in {"auto", "basic"} and cfg["username"] and cfg["password"]:
        auth = (cfg["username"], cfg["password"])
    if auth_mode in {"auto", "token"} and cfg["token"]:
        # Algumas integrações públicas do SGP usam esse header junto com app/token no body.
        headers["Authorization"] = f"*** {cfg['token']}"

    try:
        if method == "GET":
            r = requests.get(url, params=params or payload or None, headers=headers, auth=auth, timeout=cfg["timeout"])
        else:
            r = requests.request(method, url, params=params, json=payload, headers={**headers, "Content-Type": "application/json"}, auth=auth, timeout=cfg["timeout"])
        content_type = r.headers.get("content-type", "")
        try:
            data = r.json()
        except ValueError:
            data = {"raw": r.text[:2000]}
        return {
            "ok": 200 <= r.status_code < 300,
            "status_code": r.status_code,
            "content_type": content_type,
            "method": method,
            "path": path,
            "data": mask_sensitive(data),
        }
    except requests.Timeout:
        return {"ok": False, "error": "timeout", "path": path, "timeout": cfg["timeout"]}
    except requests.RequestException as e:
        return {"ok": False, "error": type(e).__name__, "message": str(e), "path": path}


@mcp.tool()
def sgp_config_status() -> Dict[str, Any]:
    """Mostra se as variáveis do SGP estão configuradas, sem expor segredo."""
    cfg = config()
    return {
        "base_url_set": bool(cfg["base_url"]),
        "basic_auth_set": bool(cfg["username"] and cfg["password"]),
        "token_auth_set": bool(cfg["app"] and cfg["token"]),
        "read_only": cfg["read_only"],
        "mask_sensitive": cfg["mask_sensitive"],
        "timeout": cfg["timeout"],
        "catalog_endpoints": len(CATALOG),
    }


@mcp.tool()
def sgp_api_catalog(category: Optional[str] = None, search: Optional[str] = None, include_dangerous: bool = False, limit: int = 50) -> Dict[str, Any]:
    """Consulta o catálogo de endpoints da documentação Postman do SGP."""
    rows = CATALOG
    if category:
        rows = [e for e in rows if category.lower() in e["category"].lower()]
    if search:
        q = search.lower()
        rows = [e for e in rows if q in (e["name"] + " " + e["path"] + " " + e["category"]).lower()]
    if not include_dangerous:
        rows = [e for e in rows if not e["dangerous_or_write"]]
    return {"total": len(rows), "items": rows[: max(1, min(limit, 200))]}


@mcp.tool()
def sgp_request(method: str, path: str, params: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None,
                auth_mode: str = "auto", allow_write: bool = False) -> Dict[str, Any]:
    """Executa uma chamada controlada à API SGP. Escrita/perigo é bloqueado quando SGP_READ_ONLY=true."""
    return request_sgp(method, path, params=params, body=body, auth_mode=auth_mode, allow_write=allow_write)


@mcp.tool()
def sgp_precadastro_planos() -> Dict[str, Any]:
    """Lista planos disponíveis para pré-cadastro."""
    return request_sgp("POST", "/api/precadastro/plano/list", name="Plano – Listar")


@mcp.tool()
def sgp_precadastro_vencimentos() -> Dict[str, Any]:
    """Lista dias/vencimentos disponíveis para pré-cadastro."""
    return request_sgp("POST", "/api/precadastro/vencimento/list", name="Vencimento – Listar")


@mcp.tool()
def sgp_precadastro_vendedores() -> Dict[str, Any]:
    """Lista vendedores disponíveis para pré-cadastro."""
    return request_sgp("POST", "/api/precadastro/vendedor/list", name="Vendedor – Listar")


@mcp.tool()
def sgp_cliente_consultar(cpfcnpj: Optional[str] = None, contrato: Optional[str] = None, nome: Optional[str] = None,
                          login: Optional[str] = None, onu_serial: Optional[str] = None) -> Dict[str, Any]:
    """Consulta cliente na URA por CPF/CNPJ, contrato, nome, login PPPoE ou serial de ONU."""
    body = {k: v for k, v in {
        "cpfcnpj": cpfcnpj, "contrato": contrato, "nome": nome, "login": login, "onu_serial": onu_serial
    }.items() if v}
    if not body:
        return {"ok": False, "error": "informe cpfcnpj, contrato, nome, login ou onu_serial"}
    return request_sgp("POST", "/api/ura/consultacliente/", body=body, name="Cliente – Consultar")


@mcp.tool()
def sgp_cliente_contratos(cpfcnpj: str) -> Dict[str, Any]:
    """Consulta contratos de um cliente por CPF/CNPJ usando endpoint CRM."""
    return request_sgp("GET", "/api/crm/cliente/contratos/", params={"cpfcnpj": cpfcnpj}, include_app_token=False, name="Consulta Contratos")


@mcp.tool()
def sgp_titulos_listar(cpfcnpj: Optional[str] = None, contrato: Optional[int] = None, cliente_id: Optional[int] = None,
                       limit: int = 10) -> Dict[str, Any]:
    """Lista títulos/faturas via URA. Retorno é mascarado por padrão."""
    body = {"limit": limit}
    if cpfcnpj: body["cpfcnpj"] = cpfcnpj
    if contrato: body["contrato"] = contrato
    if cliente_id: body["cliente_id"] = cliente_id
    return request_sgp("POST", "/api/ura/titulos/", body=body, name="Fatura – Listar")


@mcp.tool()
def sgp_os_listar(filtros: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Lista ordens de serviço com filtros opcionais do SGP."""
    return request_sgp("POST", "/api/os/list/", body=filtros or {}, name="Ordens de Serviço")


@mcp.tool()
def sgp_os_anotacoes(os_id: int) -> Dict[str, Any]:
    """Lista anotações de uma ordem de serviço."""
    return request_sgp("POST", f"/api/os/anotacoes/list/id/{os_id}/", body={}, name="Ordem de Serviço - Anotações")


@mcp.tool()
def sgp_ftth_olts() -> Dict[str, Any]:
    """Lista OLTs cadastradas no SGP."""
    return request_sgp("GET", "/api/fttx/olt/list/", include_app_token=False, name="Listar OLT")


@mcp.tool()
def sgp_ftth_onus(olt_id: Optional[int] = None) -> Dict[str, Any]:
    """Lista ONUs, opcionalmente por OLT."""
    path = f"/api/fttx/olt/{olt_id}/onu/list/" if olt_id else "/api/fttx/onu/list/"
    return request_sgp("GET", path, include_app_token=False, name="Listar ONU")


@mcp.tool()
def sgp_ftth_onu_info(id_onu: int) -> Dict[str, Any]:
    """Detalha informações de uma ONU."""
    return request_sgp("GET", f"/api/fttx/onu/{id_onu}/info/", include_app_token=False, name="ONU Info")


@mcp.tool()
def sgp_radius_status(login: Optional[str] = None, contrato: Optional[str] = None) -> Dict[str, Any]:
    """Detalha status de login PPPoE/RADIUS por login ou contrato."""
    body = {k: v for k, v in {"login": login, "contrato": contrato}.items() if v}
    return request_sgp("POST", "/ws/radius/service/status/", body=body, name="Login PPPoE – Detalhar Status")


@mcp.tool()
def sgp_cpe_detalhes(id_servico: int) -> Dict[str, Any]:
    """Consulta detalhes de CPE/serviço no Gerenciador CPE."""
    return request_sgp("GET", f"/api/cpemanager/servico/{id_servico}/infodetail", include_app_token=False, name="CPE - Detalhes")


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
