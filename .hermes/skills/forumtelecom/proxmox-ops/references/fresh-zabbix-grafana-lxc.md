# Fresh Zabbix + Grafana LXC on Proxmox

Use this when the user asks to create a new monitoring container from zero, not to repair an existing one.

## Discovery

1. Connect to Proxmox and identify node/storage/network:
   - `pveversion`
   - `pvesh get /nodes`
   - `pvesm status`
   - `pct list`
   - `cat /etc/network/interfaces`
2. Choose a free CTID with `pvesh get /cluster/nextid` and confirm it is not in `pct list`.
3. Choose a free management IP by checking existing `pct config <id>` `net0` entries and probing the candidate address.

## Container creation pattern

Example shape:

```bash
pct create <CTID> local:vztmpl/debian-12-standard_*.tar.zst \
  --hostname zabbix-grafana-novo \
  --cores 2 --memory 4096 --swap 1024 \
  --rootfs local:32 \
  --features nesting=1,keyctl=1 \
  --unprivileged 1 --onboot 1 \
  --nameserver 1.1.1.1 --searchdomain local \
  --net0 name=eth0,bridge=vmbr0,firewall=1,ip=<IP>/24,gw=<GW>,type=veth \
  --password '<generated-root-password>'
pct start <CTID>
pct exec <CTID> -- bash -lc 'hostname -I && ping -c1 -W2 1.1.1.1'
```

## Zabbix package install pattern

Inside Debian 12 LXC:

```bash
apt-get update
apt-get install -y ca-certificates curl wget gnupg lsb-release locales apt-transport-https software-properties-common
wget -q https://repo.zabbix.com/zabbix/7.0/debian/pool/main/z/zabbix-release/zabbix-release_latest_7.0+debian12_all.deb -O /tmp/zabbix-release.deb
dpkg -i /tmp/zabbix-release.deb
apt-get update
apt-get install -y postgresql postgresql-contrib zabbix-server-pgsql zabbix-frontend-php php8.2-pgsql zabbix-nginx-conf zabbix-sql-scripts zabbix-agent nginx php8.2-fpm
```

Create role/database, import schema only when empty:

```bash
su - postgres -c "createuser --pwprompt zabbix"
su - postgres -c "createdb -O zabbix zabbix"
zcat /usr/share/zabbix-sql-scripts/postgresql/server.sql.gz | PGPASSWORD='<dbpass>' psql -U zabbix -h 127.0.0.1 zabbix
```

Set `DBPassword=<dbpass>` in `/etc/zabbix/zabbix_server.conf`.

Create `/etc/zabbix/web/zabbix.conf.php` so the frontend is immediately usable:

```php
<?php
$DB['TYPE'] = 'POSTGRESQL';
$DB['SERVER'] = 'localhost';
$DB['PORT'] = '0';
$DB['DATABASE'] = 'zabbix';
$DB['USER'] = 'zabbix';
$DB['PASSWORD'] = '<dbpass>';
$DB['SCHEMA'] = '';
$DB['ENCRYPTION'] = false;
$DB['VERIFY_HOST'] = true;
$ZBX_SERVER = 'localhost';
$ZBX_SERVER_PORT = '10051';
$ZBX_SERVER_NAME = 'Zabbix <Name>';
$IMAGE_FORMAT_DEFAULT = IMAGE_FORMAT_PNG;
```

Nginx: remove `/etc/nginx/sites-enabled/default`, link `/etc/nginx/conf.d/zabbix.conf -> /etc/zabbix/nginx.conf`, ensure it listens on port 80, then `nginx -t && systemctl restart nginx php8.2-fpm zabbix-server zabbix-agent postgresql`.

## Grafana install pattern

```bash
install -d -m 0755 /etc/apt/keyrings
wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor -o /etc/apt/keyrings/grafana.gpg
echo 'deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main' > /etc/apt/sources.list.d/grafana.list
apt-get update
apt-get install -y grafana
systemctl enable --now grafana-server
grafana cli --homepath /usr/share/grafana plugins install alexanderzobnin-zabbix-app
systemctl restart grafana-server
```

If `curl` immediately after restart fails on port 3000, wait and retry health `/api/health`; Grafana can take a few seconds after plugin installation.

Enable the Zabbix app plugin with the Grafana API. If shell quoting mangles JSON, use Python/urllib or a real JSON file and verify `enabled=true`:

```bash
curl -u admin:admin http://127.0.0.1:3000/api/plugins/alexanderzobnin-zabbix-app/settings
```

## Credential hardening

- Change default Zabbix `Admin/zabbix`. On Zabbix 7.0, `user.update` requires `current_passwd`.
- Change Grafana `admin/admin` with:

```bash
grafana-cli --homepath /usr/share/grafana admin reset-admin-password '<new-password>'
```

Store final credentials in a secure password manager rather than sending them in chat.

## Verification checklist

```bash
pct status <CTID>
pct config <CTID> | egrep 'hostname|cores|memory|rootfs|net0|onboot|features'
pct exec <CTID> -- systemctl is-active zabbix-server zabbix-agent postgresql nginx php8.2-fpm grafana-server
curl -sS -o /dev/null -w 'Zabbix HTTP %{http_code} %{content_type}\n' http://<IP>/
curl -sS -o /dev/null -w 'Grafana HTTP %{http_code} %{content_type}\n' http://<IP>:3000/login
```

Also verify API login for both Zabbix and Grafana using the final stored credentials before reporting success.
