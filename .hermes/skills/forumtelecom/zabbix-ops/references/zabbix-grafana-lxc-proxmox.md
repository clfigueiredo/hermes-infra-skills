# Zabbix + Grafana em LXC Proxmox — verificação e ajustes recorrentes

Use quando o usuário pedir para subir/validar uma stack Zabbix + Grafana em container LXC no Proxmox.

## Checklist rápido

No host Proxmox:

```bash
pct status <CTID>
pct config <CTID> | egrep 'hostname|cores|memory|rootfs|net0|onboot|features'
pct exec <CTID> -- bash -lc 'systemctl is-active zabbix-server zabbix-agent postgresql nginx grafana-server'
```

Validação HTTP externa a partir do host Proxmox:

```bash
curl -sS -o /dev/null -w 'Zabbix HTTP %{http_code} %{content_type}\n' --max-time 8 http://<CT_IP>/
curl -sS -o /dev/null -w 'Grafana HTTP %{http_code} %{content_type}\n' --max-time 8 http://<CT_IP>:3000/login
```

Versões:

```bash
pct exec <CTID> -- bash -lc 'zabbix_server -V 2>&1 | head -1; grafana-server -v 2>/dev/null | head -1'
```

## Pitfall: Nginx servindo a página default em vez do Zabbix

Em instalações Debian/Nginx, o site default em `/etc/nginx/sites-enabled/default` pode capturar `listen 80 default_server` e fazer `http://<CT_IP>/` mostrar a página padrão do Debian, mesmo com `/etc/nginx/conf.d/zabbix.conf` correto.

Diagnóstico:

```bash
pct exec <CTID> -- bash -lc 'ls -la /etc/nginx/conf.d /etc/nginx/sites-enabled; nginx -T 2>/dev/null | grep -n "default_server\|root /usr/share/zabbix\|zabbix.conf" | head -50'
curl -sS --max-time 5 http://<CT_IP>/ | grep -i -m2 -E 'Zabbix|Username|nginx'
```

Correção segura:

```bash
pct exec <CTID> -- bash -lc 'if [ -L /etc/nginx/sites-enabled/default ]; then rm /etc/nginx/sites-enabled/default; fi; nginx -t'
pct exec <CTID> -- systemctl reload nginx
```

Depois confirme que a raiz mostra a tela de login do Zabbix:

```bash
curl -sS --max-time 5 http://<CT_IP>/ | grep -i -m2 -E 'Zabbix|Username|Password|Sign in'
```

## Grafana: plugin Zabbix App

Em Grafana moderno, `grafana-cli plugins install ...` pode falhar com erro de homepath. Preferir o subcomando novo com homepath explícito:

```bash
pct exec <CTID> -- bash -lc 'grafana cli --homepath /usr/share/grafana plugins install alexanderzobnin-zabbix-app'
pct exec <CTID> -- systemctl restart grafana-server
pct exec <CTID> -- bash -lc 'sleep 5; systemctl is-active grafana-server; grafana cli --homepath /usr/share/grafana plugins ls | grep alexanderzobnin-zabbix-app'
```

Habilitar o app pela API do Grafana, se houver credencial admin válida:

```bash
curl -sS -u <user>:<pass> -X POST -H 'Content-Type: application/json' \
  -d '{"enabled":true,"pinned":true}' \
  http://<CT_IP>:3000/api/plugins/alexanderzobnin-zabbix-app/settings
```

Confirmar:

```bash
curl -sS -u <user>:<pass> http://<CT_IP>:3000/api/plugins/alexanderzobnin-zabbix-app/settings \
  | jq '{id,enabled,pinned}'
```

## Login default não é prova de falha

Se `Admin / zabbix` não autenticar no Zabbix, reporte como senha já alterada/provável credencial customizada e ofereça reset/criação de usuário admin, sem assumir que a instalação está quebrada.

Para Grafana, `admin / admin` pode funcionar em instalação nova, mas deve ser trocado imediatamente em produção.
