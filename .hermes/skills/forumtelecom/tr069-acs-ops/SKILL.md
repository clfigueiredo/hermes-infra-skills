---
name: tr069-acs-ops
description: "Use when the user asks to design, install, operate, secure, monitor, or troubleshoot a TR-069/CWMP ACS environment for ISP networks: GenieACS, CPE/ONT/ONU/router onboarding, ACS URL, Inform, device parameters, presets/provisions, firmware/config push, WAN/PPPoE/Wi-Fi provisioning, API automation, Docker deployment, logs, security and Zabbix monitoring."
version: 1.0.0
author: Hermes Tutor
license: MIT
metadata:
  hermes:
    tags: [tr069, tr-069, cwmp, acs, genieacs, cpe, ont, onu, provisioning, isp, zabbix]
    related_skills: [docker-ops, zabbix-ops, olt-huawei-ops, olt-fiberhome-ops, olt-vsol-ops]
---

# TR-069 / ACS Operations

Atue como engenheiro sênior de ACS/TR-069 para provedores. Ajudar a subir servidor ACS, integrar CPEs/ONTs/roteadores, provisionar parâmetros, automatizar rotinas e diagnosticar falhas de comunicação CWMP.

Referências públicas usadas como base: GenieACS (`genieacs.com`, `docs.genieacs.com`, `github.com/genieacs/genieacs`) e práticas de ISP para TR-069/CWMP.

## Conceitos rápidos

- **TR-069 / CWMP**: protocolo de gerenciamento remoto de CPE pelo ACS.
- **ACS**: Auto Configuration Server; exemplo aberto: GenieACS.
- **CPE**: equipamento gerenciado: ONU/ONT, roteador Wi-Fi, CPE rádio, ATA etc.
- **Inform**: conexão periódica do CPE para o ACS anunciando status/eventos.
- **Connection Request**: ACS pedindo ao CPE para abrir sessão CWMP fora do inform periódico.
- **Parameter tree**: árvore de parâmetros `InternetGatewayDevice.*` ou `Device.*`.
- **Provision/Preset**: regra/script do ACS para aplicar configuração automaticamente.

## Postura operacional obrigatória

1. **Segurança primeiro**: nunca publicar senhas, ACS credentials, PPPoE, Wi-Fi PSK, serial completo em massa, tokens/API keys, MongoDB URI ou backups brutos.
2. **Ambiente de teste antes de massa**: validar em 1 equipamento, depois lote pequeno, só então produção.
3. **Backup antes de alteração**: quando possível, baixar configuração/estado do CPE antes de firmware/config push.
4. **Mudança reversível**: firmware, reset, Wi-Fi, WAN, VLAN e ACS URL podem derrubar cliente; exigir janela/rollback quando houver risco.
5. **Fonte da verdade**: modelo/firmware e árvore de parâmetros real do equipamento prevalecem sobre exemplo genérico.

## Quando usar

- subir um ACS TR-069 do zero;
- instalar GenieACS com Docker ou Linux;
- configurar ACS URL em ONT/roteador;
- diagnosticar CPE que não aparece no ACS;
- criar presets/provisions;
- alterar Wi-Fi, PPPoE, WAN, VoIP, firmware ou reboot remoto;
- integrar com IXC/ERP/RADIUS/API;
- monitorar ACS e dispositivos no Zabbix;
- criar rotina segura para gerenciar dispositivos da rede.

## Arquitetura mínima recomendada

```text
CPE/ONT/Router  --->  ACS CWMP :7547
ACS UI/API      --->  HTTP/API :7557
ACS NBI/API     --->  Integrações ERP/NOC
MongoDB         --->  banco do GenieACS
Reverse proxy   --->  TLS e autenticação para UI/API, se exposto
Firewall        --->  restringe UI/API; CWMP só de redes autorizadas
```

Portas comuns do GenieACS:

```text
7547/tcp  CWMP - endpoint usado pelos CPEs
7557/tcp  NBI/API e UI, conforme implantação
7567/tcp  FS - file server para firmware/config, quando usado
```

Expor UI/API publicamente sem autenticação e ACL é erro grave. CWMP pode ficar acessível aos CPEs, mas preferir limitar por ASN/rede do provedor/VPN.

## Subir servidor GenieACS com Docker Compose

Modelo base para laboratório ou pequeno provedor. Ajuste senhas e exposição antes de produção.

```yaml
services:
  mongo:
    image: mongo:7
    restart: unless-stopped
    volumes:
      - ./mongo-data:/data/db
    command: ["mongod", "--quiet"]

  genieacs:
    image: genieacs/genieacs:latest
    restart: unless-stopped
    depends_on:
      - mongo
    environment:
      GENIEACS_MONGODB_CONNECTION_URL: mongodb://mongo/genieacs
      GENIEACS_CWMP_ACCESS_LOG_FILE: /var/log/genieacs/genieacs-cwmp-access.log
      GENIEACS_NBI_ACCESS_LOG_FILE: /var/log/genieacs/genieacs-nbi-access.log
      GENIEACS_FS_ACCESS_LOG_FILE: /var/log/genieacs/genieacs-fs-access.log
      GENIEACS_UI_ACCESS_LOG_FILE: /var/log/genieacs/genieacs-ui-access.log
      GENIEACS_DEBUG_FILE: /var/log/genieacs/genieacs-debug.yaml
      GENIEACS_EXT_DIR: /opt/genieacs/ext
    ports:
      - "7547:7547"
      - "7557:7557"
      - "7567:7567"
    volumes:
      - ./genieacs-logs:/var/log/genieacs
      - ./genieacs-ext:/opt/genieacs/ext
```

Subir e validar:

```bash
mkdir -p /opt/genieacs/{mongo-data,genieacs-logs,genieacs-ext}
cd /opt/genieacs
# salvar compose.yaml aqui
docker compose up -d
docker compose ps
docker compose logs --tail=100 genieacs
ss -lntp | egrep ':7547|:7557|:7567'
curl -sS http://127.0.0.1:7557/devices | head
```

Critério de conclusão: containers `Up`, portas ouvindo, API respondendo e logs sem erro de MongoDB.

## Produção: reverse proxy, firewall e TLS

Recomendação:

- CWMP `7547`: liberar apenas redes dos CPEs/CGNAT/OLT/gerência, quando possível.
- UI/API `7557`: não expor aberto; usar VPN, IP allowlist, autenticação no proxy ou SSO.
- FS `7567`: expor só se precisar servir firmware/config para CPEs.
- MongoDB: nunca publicar na Internet.

Exemplo de firewall host:

```bash
# exemplo conceitual: ajuste interface/rede antes de aplicar
ufw allow from <REDE_CPE> to any port 7547 proto tcp
ufw allow from <REDE_NOC> to any port 7557 proto tcp
ufw allow from <REDE_CPE> to any port 7567 proto tcp
ufw deny 27017/tcp
```

Para proxy, usar Nginx/Traefik/Caddy com TLS e autenticação na UI/API. Não colocar Basic Auth no endpoint CWMP sem validar suporte do CPE.

## Configurar CPE/ONT para apontar ao ACS

Campos típicos no equipamento:

```text
ACS URL: http://acs.exemplo.net:7547/
Periodic Inform: enable
Periodic Inform Interval: 300 a 3600 segundos
Connection Request Username/Password: forte e único por CPE, quando suportado
ACS Username/Password: forte e único ou política definida
```

Parâmetros comuns, dependendo do firmware:

```text
InternetGatewayDevice.ManagementServer.URL
InternetGatewayDevice.ManagementServer.PeriodicInformEnable
InternetGatewayDevice.ManagementServer.PeriodicInformInterval
InternetGatewayDevice.ManagementServer.ConnectionRequestUsername
InternetGatewayDevice.ManagementServer.ConnectionRequestPassword
Device.ManagementServer.URL
Device.ManagementServer.PeriodicInformEnable
Device.ManagementServer.PeriodicInformInterval
```

Em OLT/ONT, confirmar se o TR-069 fica no roteador interno da ONT, na VLAN de gerência ou via WAN do cliente. Fabricantes variam bastante.

## Diagnóstico: CPE não aparece no ACS

Checklist na ordem:

```text
1. CPE tem ACS URL correto? Protocolo, host, porta e barra final.
2. DNS resolve no CPE?
3. CPE alcança TCP/7547 no servidor?
4. Firewall/NAT/CGNAT bloqueia saída?
5. Horário/NTP do CPE está muito errado?
6. Credenciais ACS batem?
7. O CPE usa Device.* ou InternetGatewayDevice.*?
8. Logs do CWMP mostram request, 401, timeout ou erro SOAP?
```

Comandos no servidor:

```bash
docker compose logs -f genieacs
# ou, se instalado nativo:
journalctl -u genieacs-cwmp -f

tcpdump -ni any tcp port 7547
ss -lntp | grep 7547
curl -sS http://127.0.0.1:7557/devices | jq '.[0] // empty'
```

Interpretação rápida:

```text
Sem pacote no tcpdump: problema rede/DNS/ACS URL/firewall.
Pacote chega mas sem cadastro: ver log CWMP e autenticação.
401 repetido: usuário/senha ACS divergente.
Sessão inicia e falha SOAP: firmware/parameter tree/vendor quirk.
Aparece mas sem parâmetros: precisa refresh/getParameterValues.
```

## Operação via API GenieACS

Listar dispositivos:

```bash
curl -sS 'http://127.0.0.1:7557/devices?projection=_id,InternetGatewayDevice.DeviceInfo.SerialNumber,Device.DeviceInfo.SerialNumber' | jq .
```

Buscar por serial/modelo exige URL encode na query. Exemplo genérico:

```bash
QUERY='{"_id":{"$regex":"SERIAL_OU_MAC"}}'
curl -G 'http://127.0.0.1:7557/devices' --data-urlencode "query=$QUERY" | jq .
```

Criar task de refresh em um device:

```bash
DEVICE_ID='<id-url-encoded>'
curl -sS -X POST "http://127.0.0.1:7557/devices/$DEVICE_ID/tasks?connection_request" \
  -H 'Content-Type: application/json' \
  --data '{"name":"refreshObject","objectName":""}' | jq .
```

Reboot remoto, somente com confirmação:

```bash
curl -sS -X POST "http://127.0.0.1:7557/devices/$DEVICE_ID/tasks?connection_request" \
  -H 'Content-Type: application/json' \
  --data '{"name":"reboot"}' | jq .
```

Nunca rodar task em lote sem filtro validado e contagem prévia.

## Provisions e presets

Use presets para aplicar regras automáticas por modelo, tag, serial, OUI, firmware ou primeiro inform.

Padrão seguro:

```text
1. Criar tag de teste: LAB-TR069
2. Aplicar preset só nessa tag/modelo
3. Testar em 1 CPE
4. Verificar parâmetros e logs
5. Expandir para lote pequeno
6. Documentar rollback
```

Exemplo conceitual de provision GenieACS:

```javascript
// Exemplo conceitual. Validar parameter tree real antes de usar.
const now = Date.now();

// Garantir que dados básicos estejam recentes
declare('InternetGatewayDevice.DeviceInfo.SerialNumber', {value: now});
declare('InternetGatewayDevice.DeviceInfo.SoftwareVersion', {value: now});

// Ajustar periodic inform
declare('InternetGatewayDevice.ManagementServer.PeriodicInformEnable', null, {value: true});
declare('InternetGatewayDevice.ManagementServer.PeriodicInformInterval', null, {value: 900});
```

Para Wi-Fi/PPPoE/VLAN, nunca presumir caminho do parâmetro. Primeiro descobrir árvore do dispositivo:

```text
InternetGatewayDevice.LANDevice.*
InternetGatewayDevice.WANDevice.*
InternetGatewayDevice.WANDevice.1.WANConnectionDevice.*
Device.WiFi.*
Device.PPP.Interface.*
Device.Ethernet.*
```

## Rotinas comuns de gerenciamento

### Trocar SSID/senha Wi-Fi

1. identificar se o CPE usa `InternetGatewayDevice.LANDevice...WLANConfiguration` ou `Device.WiFi.SSID/AccessPoint`;
2. ler valores atuais;
3. aplicar em um CPE de teste;
4. validar cliente reconectado;
5. expandir por modelo/firmware.

### Configurar PPPoE/WAN

1. mapear interface WAN correta;
2. confirmar VLAN/tagging feito pela ONT/roteador/OLT;
3. não expor usuário/senha PPPoE;
4. aplicar só no CPE correto;
5. validar autenticação no RADIUS/BNG/BRAS.

### Firmware push

1. conferir modelo/hardware revision;
2. subir arquivo no FS/URL acessível;
3. testar checksum/tamanho;
4. aplicar em laboratório;
5. agendar janela;
6. não atualizar lote grande sem rollback.

## Integração com ERP/RADIUS/IXC/NOC

Padrão recomendado:

```text
ERP/IXC/RADIUS → gera dados do assinante/plano
Automação → consulta GenieACS API
ACS → aplica tag/preset/provision no CPE
Zabbix/NOC → monitora disponibilidade e falhas
```

Regras de segurança:

- tokens/API keys em `.env` ou cofre, nunca no grupo;
- logs sem PPPoE password/Wi-Fi PSK;
- auditoria de quem alterou preset/provision;
- limite/rate-limit em automação de lote.

## Monitoramento Zabbix

Itens mínimos para o servidor ACS:

```text
porta 7547 ouvindo
porta 7557/API respondendo
porta 7567, se usada
containers/systemd services UP
MongoDB UP e uso de disco
logs com taxa de erro 4xx/5xx/SOAP fault
quantidade de devices informando nas últimas X horas
fila/tasks pendentes
CPU/RAM/disco
backup recente
```

Consulta útil para contar devices recentes depende do banco/modelo usado; preferir API/consulta controlada e validar em laboratório.

## Backup e restore

Backup mínimo:

```bash
# Docker Compose
cd /opt/genieacs
docker compose exec mongo mongodump --archive=/tmp/genieacs.archive --db=genieacs
docker compose cp mongo:/tmp/genieacs.archive ./backup-genieacs-$(date +%F).archive
tar czf backup-genieacs-files-$(date +%F).tar.gz compose.yaml genieacs-ext genieacs-logs 2>/dev/null || true
```

Restore deve ser testado em ambiente separado antes de produção.

## Comandos perigosos — exigir confirmação

Não executar sem confirmação explícita:

```text
reset/factory reset de CPE
reboot em massa
firmware upgrade/downgrade
alterar ACS URL em lote
alterar WAN/PPPoE/VLAN/Wi-Fi em lote
apagar devices/tasks/presets/provisions
expor UI/API publicamente
restore de banco em produção
```

## Relatório final padrão

```text
Status: OK/atenção/falha
ACS: <GenieACS versão/host>
CPEs: <total/novos/sem inform>
Ação: <instalado/configurado/diagnosticado>
Validação: <porta/API/log/device inform>
Risco: <se houver>
Próximo passo: <objetivo>
```

## Armadilhas comuns

1. **Confundir TR-069 com SNMP**: TR-069 é sessão iniciada pelo CPE; SNMP é consulta ativa do NOC.
2. **Publicar UI/API sem proteção**: risco crítico.
3. **Parameter tree diferente por fabricante**: não reaproveitar provision sem mapear modelo/firmware.
4. **Connection request não funciona atrás de NAT**: depende de como o CPE expõe/recebe conexão; periodic inform costuma ser mais confiável.
5. **Firmware errado**: pode brickar CPE.
6. **Preset amplo demais**: aplicar por tag/modelo/lote pequeno primeiro.
7. **Sem NTP/DNS no CPE**: causa falha de conexão, TLS, logs confusos e inform irregular.
8. **Banco sem backup**: perder MongoDB significa perder histórico, presets e estado operacional.

## Checklist de validação

- [ ] ACS instalado e portas necessárias ouvindo;
- [ ] UI/API protegida por ACL/VPN/auth;
- [ ] MongoDB persistente e com backup;
- [ ] CPE de teste apareceu no ACS;
- [ ] parâmetros básicos lidos;
- [ ] preset/provision testado em tag/lote pequeno;
- [ ] logs CWMP sem erros críticos;
- [ ] Zabbix/NOC monitorando serviços e capacidade;
- [ ] relatório final sem segredos.
