"""NOC customer diagnostics plugin for Hermes Agent.

Read-only tools for an ISP/NOC dashboard. Equipment/ERP-specific collection is
proxied through an optional internal API configured by NOC_DIAG_API_BASE_URL.
DNS/HTTP latency checks run locally from the Hermes host.
"""

from __future__ import annotations

import json
import os
import socket
import ssl
import subprocess
import time
import urllib.error
import urllib.request
from typing import Any, Dict, List, Tuple

PLUGIN_TOOLSET = "noc_customer_diagnostics"
DEFAULT_META_DOMAINS = [
    "facebook.com",
    "instagram.com",
    "whatsapp.com",
    "messenger.com",
]
DEFAULT_HTTP_URLS = [
    "https://www.facebook.com/",
    "https://www.instagram.com/",
    "https://www.whatsapp.com/",
    "https://www.messenger.com/",
]


def _json(data: Dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def _clean_login(value: str) -> str:
    value = (value or "").strip()
    if not value:
        raise ValueError("login PPPoE vazio")
    if len(value) > 128:
        raise ValueError("login PPPoE muito longo")
    return value


def _mask(value: str, keep_start: int = 3, keep_end: int = 2) -> str:
    value = str(value or "")
    if len(value) <= keep_start + keep_end:
        return "***"
    return value[:keep_start] + "***" + value[-keep_end:]


def _api_base() -> str:
    return (os.getenv("NOC_DIAG_API_BASE_URL") or "").strip().rstrip("/")


def _api_token() -> str:
    return (os.getenv("NOC_DIAG_API_TOKEN") or "").strip()


def _api_timeout() -> float:
    try:
        return float(os.getenv("NOC_DIAG_TIMEOUT", "15"))
    except ValueError:
        return 15.0


def _read_only() -> bool:
    return (os.getenv("NOC_DIAG_READ_ONLY", "true").strip().lower() not in {"0", "false", "no", "off"})


def _api_post(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    base = _api_base()
    if not base:
        return {
            "ok": False,
            "status": "not_configured",
            "message": "NOC_DIAG_API_BASE_URL não configurado; ferramenta retornou sem consultar equipamentos.",
            "expected_endpoint": path,
        }

    url = f"{base}{path}"
    safe_payload = dict(payload)
    safe_payload["read_only"] = _read_only()
    body = json.dumps(safe_payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Hermes-NOC-Diagnostics/0.1",
    }
    token = _api_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"

    started = time.perf_counter()
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=_api_timeout()) as resp:
            raw = resp.read(1024 * 512).decode("utf-8", "replace")
            elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
            try:
                data = json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                data = {"raw": raw[:4000]}
            return {
                "ok": 200 <= resp.status < 300,
                "status": resp.status,
                "latency_ms": elapsed_ms,
                "endpoint": path,
                "data": data,
            }
    except urllib.error.HTTPError as exc:
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        detail = exc.read(4096).decode("utf-8", "replace") if exc.fp else ""
        return {"ok": False, "status": exc.code, "latency_ms": elapsed_ms, "endpoint": path, "error": detail[:1000]}
    except Exception as exc:
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        return {"ok": False, "status": "error", "latency_ms": elapsed_ms, "endpoint": path, "error": f"{type(exc).__name__}: {exc}"}


def _split_list(value: Any, default: List[str]) -> List[str]:
    if value is None or value == "":
        return list(default)
    if isinstance(value, str):
        parts = [p.strip() for p in value.replace("\n", ",").split(",")]
    elif isinstance(value, list):
        parts = [str(p).strip() for p in value]
    else:
        parts = []
    return [p for p in parts if p]


def _resolve_system(domain: str, timeout: float) -> Dict[str, Any]:
    started = time.perf_counter()
    try:
        old_timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(timeout)
        try:
            infos = socket.getaddrinfo(domain, 443, type=socket.SOCK_STREAM)
        finally:
            socket.setdefaulttimeout(old_timeout)
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        ips = sorted({i[4][0] for i in infos})[:10]
        return {"ok": True, "resolver": "system", "domain": domain, "latency_ms": elapsed_ms, "ips": ips}
    except Exception as exc:
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        return {"ok": False, "resolver": "system", "domain": domain, "latency_ms": elapsed_ms, "error": f"{type(exc).__name__}: {exc}"}


def _resolve_with_dig(domain: str, resolver: str, timeout: float) -> Dict[str, Any]:
    started = time.perf_counter()
    cmd = ["dig", f"@{resolver}", domain, "A", "+short", f"+time={max(1, int(timeout))}", "+tries=1"]
    try:
        proc = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout + 1)
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        ips = [line.strip() for line in proc.stdout.splitlines() if line.strip() and not line.startswith(";")]
        return {
            "ok": proc.returncode == 0 and bool(ips),
            "resolver": resolver,
            "domain": domain,
            "latency_ms": elapsed_ms,
            "ips": ips[:10],
            "stderr": proc.stderr.strip()[:500] if proc.stderr else "",
        }
    except FileNotFoundError:
        return {"ok": False, "resolver": resolver, "domain": domain, "error": "comando dig não instalado"}
    except Exception as exc:
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        return {"ok": False, "resolver": resolver, "domain": domain, "latency_ms": elapsed_ms, "error": f"{type(exc).__name__}: {exc}"}


def _http_check(url: str, timeout: float) -> Dict[str, Any]:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    started = time.perf_counter()
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Hermes-NOC-Diagnostics/0.1"})
    try:
        context = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=timeout, context=context) as resp:
            elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
            return {"ok": True, "url": url, "status": resp.status, "latency_ms": elapsed_ms, "final_url": resp.geturl()}
    except urllib.error.HTTPError as exc:
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        # HTTP error still proves DNS/TCP/TLS path reached the service.
        return {"ok": exc.code < 500, "url": url, "status": exc.code, "latency_ms": elapsed_ms, "final_url": exc.geturl()}
    except Exception as exc:
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        return {"ok": False, "url": url, "latency_ms": elapsed_ms, "error": f"{type(exc).__name__}: {exc}"}


def _grade_radio(data: Dict[str, Any]) -> Tuple[str, List[str]]:
    notes: List[str] = []
    status = "unknown"
    rx = data.get("signal_dbm") or data.get("rx_signal_dbm") or data.get("signal")
    ccq = data.get("ccq") or data.get("tx_ccq")
    noise = data.get("noise_floor_dbm") or data.get("noise")
    try:
        rx_f = float(str(rx).replace("dBm", "").strip()) if rx is not None else None
    except Exception:
        rx_f = None
    try:
        ccq_f = float(str(ccq).replace("%", "").strip()) if ccq is not None else None
    except Exception:
        ccq_f = None
    try:
        noise_f = float(str(noise).replace("dBm", "").strip()) if noise is not None else None
    except Exception:
        noise_f = None

    if rx_f is not None:
        if rx_f <= -75:
            status = "bad"
            notes.append(f"sinal fraco ({rx_f} dBm)")
        elif rx_f <= -68:
            status = "attention"
            notes.append(f"sinal marginal ({rx_f} dBm)")
        else:
            status = "good"
            notes.append(f"sinal bom ({rx_f} dBm)")
    if ccq_f is not None:
        if ccq_f < 70:
            status = "bad"
            notes.append(f"CCQ baixo ({ccq_f}%)")
        elif ccq_f < 85 and status != "bad":
            status = "attention"
            notes.append(f"CCQ em atenção ({ccq_f}%)")
        else:
            notes.append(f"CCQ bom ({ccq_f}%)")
    if noise_f is not None:
        notes.append(f"ruído {noise_f} dBm")
    return status, notes


def _summarize(login: str, pppoe: Dict[str, Any], logs: Dict[str, Any], signal: Dict[str, Any], port: Dict[str, Any], dns: Dict[str, Any], http: Dict[str, Any]) -> Dict[str, Any]:
    findings: List[str] = []
    risks: List[str] = []
    recommendations: List[str] = []

    p_data = pppoe.get("data") if isinstance(pppoe.get("data"), dict) else {}
    online = p_data.get("online") or p_data.get("status") in {"online", "connected", "up"}
    if pppoe.get("ok") and online:
        findings.append("PPPoE online")
    elif pppoe.get("status") == "not_configured":
        findings.append("consulta PPPoE não configurada no adapter")
    else:
        risks.append("PPPoE offline ou não confirmado")
        recommendations.append("validar autenticação Radius/BNG e últimas quedas")

    s_data = signal.get("data") if isinstance(signal.get("data"), dict) else {}
    radio_status, radio_notes = _grade_radio(s_data)
    if radio_notes:
        findings.extend(radio_notes)
    if radio_status == "bad":
        risks.append("sinal/RF ruim")
        recommendations.append("verificar alinhamento, visada, interferência e canal do AP")
    elif radio_status == "attention":
        risks.append("sinal/RF em atenção")

    port_data = port.get("data") if isinstance(port.get("data"), dict) else {}
    crc = port_data.get("crc_errors") or port_data.get("rx_crc_errors") or port_data.get("errors")
    try:
        crc_i = int(crc) if crc is not None else 0
    except Exception:
        crc_i = 0
    if crc_i > 0:
        risks.append(f"porta/cabo com erros ({crc_i})")
        recommendations.append("verificar cabo, conector, negociação e PoE do AP")

    dns_results = dns.get("results") or []
    dns_failures = [r for r in dns_results if not r.get("ok")]
    if dns_results and not dns_failures:
        findings.append("DNS resolveu os domínios testados")
    elif dns_failures:
        risks.append("falha ou lentidão de DNS em parte dos domínios")
        recommendations.append("validar recursivos do provedor e comparar com DNS público")

    http_results = http.get("results") or []
    http_failures = [r for r in http_results if not r.get("ok")]
    if http_results and not http_failures:
        findings.append("HTTP/HTTPS para destinos META respondeu")
    elif http_failures:
        risks.append("falha HTTP/HTTPS em parte dos destinos META")
        recommendations.append("validar rota, CGNAT, IPv6, DNS e possível bloqueio/CDN")

    incomplete_sources = [
        name for name, block in {
            "PPPoE": pppoe,
            "logs PPPoE": logs,
            "sinal AP": signal,
            "porta AP": port,
        }.items()
        if block.get("status") == "not_configured"
    ]

    if incomplete_sources and not risks:
        health = "incompleto"
        opinion = "Testes externos de DNS/HTTP executaram, mas as consultas internas ainda não estão conectadas ao adapter NOC. Não conclua saúde do cliente sem PPPoE/AP/porta."
        recommendations.append("configurar NOC_DIAG_API_BASE_URL e endpoints internos para PPPoE/AP/porta")
    elif not risks:
        health = "saudável"
        opinion = "Conexão aparenta saudável nos testes disponíveis. Sem indício forte de falha na última milha."
    elif any("PPPoE offline" in r or "sinal/RF ruim" in r or "porta/cabo" in r for r in risks):
        health = "ruim"
        opinion = "Há indício técnico relevante na conexão do cliente. Priorizar correção da camada indicada antes de tratar como problema externo."
    else:
        health = "atenção"
        opinion = "Conexão requer atenção. Alguns testes falharam ou não foram conclusivos."

    return {
        "login_masked": _mask(login),
        "health": health,
        "opinion": opinion,
        "findings": findings,
        "risks": risks,
        "recommendations": list(dict.fromkeys(recommendations)),
    }


def handle_pppoe_lookup(args: Dict[str, Any], **kwargs) -> str:
    login = _clean_login(args.get("login", ""))
    return _json(_api_post(os.getenv("NOC_DIAG_ENDPOINT_PPPOE_LOOKUP", "/pppoe/lookup"), {"login": login}))


def handle_pppoe_disconnect_logs(args: Dict[str, Any], **kwargs) -> str:
    login = _clean_login(args.get("login", ""))
    hours = int(args.get("hours", 24) or 24)
    return _json(_api_post(os.getenv("NOC_DIAG_ENDPOINT_PPPOE_LOGS", "/pppoe/disconnect-logs"), {"login": login, "hours": max(1, min(hours, 168))}))


def handle_ap_client_signal(args: Dict[str, Any], **kwargs) -> str:
    login = _clean_login(args.get("login", ""))
    mac = (args.get("mac") or "").strip()
    return _json(_api_post(os.getenv("NOC_DIAG_ENDPOINT_AP_SIGNAL", "/ap/client-signal"), {"login": login, "mac": mac}))


def handle_ap_port_health(args: Dict[str, Any], **kwargs) -> str:
    ap_id = (args.get("ap_id") or args.get("host") or "").strip()
    interface = (args.get("interface") or "").strip()
    login = (args.get("login") or "").strip()
    if not (ap_id or login):
        raise ValueError("informe ap_id/host ou login")
    return _json(_api_post(os.getenv("NOC_DIAG_ENDPOINT_AP_PORT", "/ap/port-health"), {"ap_id": ap_id, "interface": interface, "login": login}))


def handle_dns_latency_test(args: Dict[str, Any], **kwargs) -> str:
    domains = _split_list(args.get("domains"), DEFAULT_META_DOMAINS)
    resolvers = _split_list(args.get("resolvers"), [])
    timeout = float(args.get("timeout", 5) or 5)
    results: List[Dict[str, Any]] = []
    for domain in domains[:20]:
        results.append(_resolve_system(domain, timeout))
        for resolver in resolvers[:5]:
            results.append(_resolve_with_dig(domain, resolver, timeout))
    return _json({"ok": all(r.get("ok") for r in results) if results else False, "results": results})


def handle_http_latency_test(args: Dict[str, Any], **kwargs) -> str:
    urls = _split_list(args.get("urls"), DEFAULT_HTTP_URLS)
    timeout = float(args.get("timeout", 8) or 8)
    results = [_http_check(url, timeout) for url in urls[:20]]
    return _json({"ok": all(r.get("ok") for r in results) if results else False, "results": results})


def handle_customer_connection_diagnostic(args: Dict[str, Any], **kwargs) -> str:
    login = _clean_login(args.get("login", ""))
    domains = _split_list(args.get("domains"), DEFAULT_META_DOMAINS)
    urls = _split_list(args.get("urls"), DEFAULT_HTTP_URLS)
    resolvers = _split_list(args.get("resolvers"), [])

    pppoe = json.loads(handle_pppoe_lookup({"login": login}))
    logs = json.loads(handle_pppoe_disconnect_logs({"login": login, "hours": args.get("hours", 24)}))
    signal = json.loads(handle_ap_client_signal({"login": login, "mac": args.get("mac", "")}))
    port = json.loads(handle_ap_port_health({"login": login, "ap_id": args.get("ap_id", ""), "interface": args.get("interface", "")}))
    dns = json.loads(handle_dns_latency_test({"domains": domains, "resolvers": resolvers, "timeout": args.get("dns_timeout", 5)}))
    http = json.loads(handle_http_latency_test({"urls": urls, "timeout": args.get("http_timeout", 8)}))
    summary = _summarize(login, pppoe, logs, signal, port, dns, http)

    return _json({
        "ok": True,
        "read_only": _read_only(),
        "login_masked": _mask(login),
        "summary": summary,
        "pppoe": pppoe,
        "disconnect_logs": logs,
        "ap_signal": signal,
        "ap_port": port,
        "dns": dns,
        "http": http,
    })


def _schema(name: str, description: str, properties: Dict[str, Any], required: List[str] | None = None) -> Dict[str, Any]:
    return {
        "name": name,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": properties,
            "required": required or [],
        },
    }


LOGIN_PROP = {"type": "string", "description": "Login PPPoE do cliente. Não envie senha."}

PPPOE_LOOKUP_SCHEMA = _schema(
    "pppoe_lookup",
    "Consulta read-only da sessão PPPoE: status, IP, uptime, NAS/BNG e dados operacionais retornados pela API interna.",
    {"login": LOGIN_PROP},
    ["login"],
)

PPPOE_LOGS_SCHEMA = _schema(
    "pppoe_disconnect_logs",
    "Consulta logs de desconexão PPPoE/Radius para o login informado, limitado ao período solicitado.",
    {"login": LOGIN_PROP, "hours": {"type": "integer", "description": "Janela em horas, padrão 24, máximo 168."}},
    ["login"],
)

AP_SIGNAL_SCHEMA = _schema(
    "ap_client_signal",
    "Consulta sinal/CCQ/ruído do cliente dentro do AP ou rádio onde ele está associado, via API interna.",
    {"login": LOGIN_PROP, "mac": {"type": "string", "description": "MAC do CPE/cliente, opcional quando a API consegue mapear pelo login."}},
    ["login"],
)

AP_PORT_SCHEMA = _schema(
    "ap_port_health",
    "Verifica saúde da porta/cabo do AP: link, negociação, CRC/erros, flaps e eventos de log, via API interna.",
    {
        "login": {"type": "string", "description": "Login PPPoE para mapear AP automaticamente, opcional se ap_id for informado."},
        "ap_id": {"type": "string", "description": "Identificador/host do AP."},
        "interface": {"type": "string", "description": "Interface/porta do AP, opcional."},
    },
)

DNS_SCHEMA = _schema(
    "dns_latency_test",
    "Mede tempo de resolução DNS para domínios, usando resolver do sistema e opcionalmente resolvers específicos com dig.",
    {
        "domains": {"type": "array", "items": {"type": "string"}, "description": "Domínios para testar. Padrão: redes sociais da META."},
        "resolvers": {"type": "array", "items": {"type": "string"}, "description": "Resolvers opcionais, exemplo ['1.1.1.1','8.8.8.8']."},
        "timeout": {"type": "number", "description": "Timeout por consulta em segundos."},
    },
)

HTTP_SCHEMA = _schema(
    "http_latency_test",
    "Mede latência HTTP/HTTPS para URLs, útil para Facebook/Instagram/WhatsApp e outros destinos.",
    {
        "urls": {"type": "array", "items": {"type": "string"}, "description": "URLs para testar. Padrão: principais domínios META."},
        "timeout": {"type": "number", "description": "Timeout por URL em segundos."},
    },
)

DIAGNOSTIC_SCHEMA = _schema(
    "customer_connection_diagnostic",
    "Executa diagnóstico completo read-only por login PPPoE: sessão/logs, AP/sinal/porta, DNS, HTTP e opinião consolidada.",
    {
        "login": LOGIN_PROP,
        "mac": {"type": "string", "description": "MAC opcional do CPE/cliente."},
        "ap_id": {"type": "string", "description": "AP opcional quando conhecido."},
        "interface": {"type": "string", "description": "Interface opcional do AP."},
        "hours": {"type": "integer", "description": "Janela dos logs PPPoE em horas."},
        "domains": {"type": "array", "items": {"type": "string"}, "description": "Domínios DNS opcionais."},
        "urls": {"type": "array", "items": {"type": "string"}, "description": "URLs HTTP opcionais."},
        "resolvers": {"type": "array", "items": {"type": "string"}, "description": "Resolvers DNS opcionais."},
    },
    ["login"],
)


def check_requirements() -> bool:
    # Always available: tools can return not_configured for equipment APIs and
    # still run local DNS/HTTP tests. Production should set NOC_DIAG_API_BASE_URL.
    return True


def register(ctx) -> None:
    tools = [
        ("pppoe_lookup", PPPOE_LOOKUP_SCHEMA, handle_pppoe_lookup, "🔐"),
        ("pppoe_disconnect_logs", PPPOE_LOGS_SCHEMA, handle_pppoe_disconnect_logs, "📜"),
        ("ap_client_signal", AP_SIGNAL_SCHEMA, handle_ap_client_signal, "📡"),
        ("ap_port_health", AP_PORT_SCHEMA, handle_ap_port_health, "🔌"),
        ("dns_latency_test", DNS_SCHEMA, handle_dns_latency_test, "🧭"),
        ("http_latency_test", HTTP_SCHEMA, handle_http_latency_test, "🌐"),
        ("customer_connection_diagnostic", DIAGNOSTIC_SCHEMA, handle_customer_connection_diagnostic, "🩺"),
    ]
    for name, schema, handler, emoji in tools:
        ctx.register_tool(
            name=name,
            toolset=PLUGIN_TOOLSET,
            schema=schema,
            handler=handler,
            check_fn=check_requirements,
            emoji=emoji,
        )
