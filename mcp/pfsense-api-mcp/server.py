#!/usr/bin/env python3
"""Read-first MCP server for pfSense REST API package/pfrest.

Environment:
  PFSENSE_BASE_URL=https://fw.example.com
  PFSENSE_USERNAME=admin              # optional basic/JWT username
  PFSENSE_PASSWORD=secret             # optional basic/JWT password
  PFSENSE_API_KEY=key                 # optional API key
  PFSENSE_API_SECRET=secret           # optional API secret
  PFSENSE_TOKEN=jwt-or-bearer         # optional bearer token
  PFSENSE_VERIFY_SSL=false
  PFSENSE_TIMEOUT=20
  PFSENSE_READ_ONLY=true
  PFSENSE_MASK_SENSITIVE=true
"""
from __future__ import annotations

import json
import os
import re
from typing import Any, Dict, Optional

import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("pfsense-api-mcp")

CATALOG = [
    {"name": "system_status", "method": "GET", "path": "/api/v2/status/system", "category": "system", "dangerous": False},
    {"name": "interfaces", "method": "GET", "path": "/api/v2/interface", "category": "interfaces", "dangerous": False},
    {"name": "gateways", "method": "GET", "path": "/api/v2/routing/gateway", "category": "routing", "dangerous": False},
    {"name": "firewall_rules", "method": "GET", "path": "/api/v2/firewall/rule", "category": "firewall", "dangerous": False},
    {"name": "firewall_aliases", "method": "GET", "path": "/api/v2/firewall/alias", "category": "firewall", "dangerous": False},
    {"name": "nat_port_forwards", "method": "GET", "path": "/api/v2/firewall/nat/port_forward", "category": "nat", "dangerous": False},
    {"name": "dhcp_leases", "method": "GET", "path": "/api/v2/services/dhcp_server/lease", "category": "dhcp", "dangerous": False},
    {"name": "services", "method": "GET", "path": "/api/v2/services", "category": "services", "dangerous": False},
]

DANGEROUS_RE = re.compile(r"(delete|del|remove|clear|kill|reboot|halt|poweroff|upgrade|update|restore|apply|reload|restart|stop|disable|enable|add|create|set|edit|patch|post|put)", re.I)
SENSITIVE_KEY_RE = re.compile(r"(token|secret|password|passwd|senha|key|auth|cookie|csrf|cert|private|cpf|cnpj|email|phone|telefone)", re.I)


def env_bool(name: str, default: bool = False) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return v.strip().lower() in {"1", "true", "yes", "sim", "on"}


def config() -> Dict[str, Any]:
    return {
        "base_url": os.getenv("PFSENSE_BASE_URL", "").rstrip("/"),
        "username": os.getenv("PFSENSE_USERNAME"),
        "password": os.getenv("PFSENSE_PASSWORD"),
        "api_key": os.getenv("PFSENSE_API_KEY"),
        "api_secret": os.getenv("PFSENSE_API_SECRET"),
        "token": os.getenv("PFSENSE_TOKEN"),
        "verify_ssl": env_bool("PFSENSE_VERIFY_SSL", False),
        "timeout": int(os.getenv("PFSENSE_TIMEOUT", "20")),
        "read_only": env_bool("PFSENSE_READ_ONLY", True),
        "mask_sensitive": env_bool("PFSENSE_MASK_SENSITIVE", True),
    }


def mask_value(value: Any) -> Any:
    if value is None:
        return value
    text = str(value)
    if len(text) <= 4:
        return "***"
    return text[:2] + "***" + text[-2:]


def mask_sensitive(obj: Any) -> Any:
    if not config()["mask_sensitive"]:
        return obj
    if isinstance(obj, dict):
        return {k: (mask_value(v) if SENSITIVE_KEY_RE.search(str(k)) else mask_sensitive(v)) for k, v in obj.items()}
    if isinstance(obj, list):
        return [mask_sensitive(v) for v in obj]
    return obj


def is_dangerous(method: str, path: str, name: str = "") -> bool:
    text = f"{method} {path} {name}"
    if method.upper() not in {"GET", "HEAD", "OPTIONS"}:
        return True
    return bool(DANGEROUS_RE.search(text))


def request_pfsense(method: str, path: str, *, params: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None,
                    allow_write: bool = False, auth_mode: str = "auto") -> Dict[str, Any]:
    cfg = config()
    method = method.upper()
    if not cfg["base_url"]:
        return {"ok": False, "error": "PFSENSE_BASE_URL não configurado"}
    if not path.startswith("/"):
        path = "/" + path
    if cfg["read_only"] and not allow_write and is_dangerous(method, path):
        return {"ok": False, "blocked": True, "reason": "PFSENSE_READ_ONLY=true bloqueou endpoint de escrita/perigoso", "method": method, "path": path}

    headers = {"Accept": "application/json"}
    auth = None
    if auth_mode in {"auto", "bearer"} and cfg["token"]:
        headers["Authorization"] = f"Bearer {cfg['token']}"
    elif auth_mode in {"auto", "api_key"} and cfg["api_key"] and cfg["api_secret"]:
        headers["X-API-Key"] = cfg["api_key"]
        headers["X-API-Secret"] = cfg["api_secret"]
    elif auth_mode in {"auto", "basic"} and cfg["username"] and cfg["password"]:
        auth = (cfg["username"], cfg["password"])

    try:
        r = requests.request(
            method,
            cfg["base_url"] + path,
            params=params,
            json=body if method not in {"GET", "HEAD"} else None,
            headers=headers,
            auth=auth,
            verify=cfg["verify_ssl"],
            timeout=cfg["timeout"],
        )
        try:
            data = r.json()
        except ValueError:
            data = {"raw": r.text[:2000]}
        return {"ok": 200 <= r.status_code < 300, "status_code": r.status_code, "method": method, "path": path, "data": mask_sensitive(data)}
    except requests.Timeout:
        return {"ok": False, "error": "timeout", "timeout": cfg["timeout"], "path": path}
    except requests.RequestException as exc:
        return {"ok": False, "error": type(exc).__name__, "message": str(exc), "path": path}


@mcp.tool()
def pfsense_config_status() -> Dict[str, Any]:
    """Mostra configuração do MCP pfSense sem expor segredos."""
    cfg = config()
    return {
        "base_url_set": bool(cfg["base_url"]),
        "basic_auth_set": bool(cfg["username"] and cfg["password"]),
        "api_key_auth_set": bool(cfg["api_key"] and cfg["api_secret"]),
        "bearer_token_set": bool(cfg["token"]),
        "verify_ssl": cfg["verify_ssl"],
        "timeout": cfg["timeout"],
        "read_only": cfg["read_only"],
        "mask_sensitive": cfg["mask_sensitive"],
        "catalog_endpoints": len(CATALOG),
    }


@mcp.tool()
def pfsense_endpoint_catalog(category: Optional[str] = None, search: Optional[str] = None, include_dangerous: bool = False, limit: int = 50) -> Dict[str, Any]:
    """Lista endpoints comuns do pfSense REST API package/pfrest usados por este MCP."""
    rows = CATALOG
    if category:
        rows = [r for r in rows if category.lower() in r["category"].lower()]
    if search:
        q = search.lower()
        rows = [r for r in rows if q in (r["name"] + " " + r["path"] + " " + r["category"]).lower()]
    if not include_dangerous:
        rows = [r for r in rows if not r["dangerous"]]
    return {"total": len(rows), "items": rows[: max(1, min(limit, 200))]}


@mcp.tool()
def pfsense_request(method: str, path: str, params: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None,
                    allow_write: bool = False, auth_mode: str = "auto") -> Dict[str, Any]:
    """Executa chamada controlada à API pfSense. Escrita/perigo é bloqueado por padrão."""
    return request_pfsense(method, path, params=params, body=body, allow_write=allow_write, auth_mode=auth_mode)


@mcp.tool()
def pfsense_system_status() -> Dict[str, Any]:
    """Consulta status básico do pfSense via REST API package, quando disponível."""
    return request_pfsense("GET", "/api/v2/status/system")


@mcp.tool()
def pfsense_firewall_rules() -> Dict[str, Any]:
    """Lista regras de firewall via REST API package, quando disponível."""
    return request_pfsense("GET", "/api/v2/firewall/rule")


@mcp.tool()
def pfsense_firewall_aliases() -> Dict[str, Any]:
    """Lista aliases de firewall via REST API package, quando disponível."""
    return request_pfsense("GET", "/api/v2/firewall/alias")


@mcp.tool()
def pfsense_dhcp_leases() -> Dict[str, Any]:
    """Lista leases DHCP via REST API package, quando disponível."""
    return request_pfsense("GET", "/api/v2/services/dhcp_server/lease")


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
