---
name: sophos-firewall-ops
description: "Senior Sophos Firewall/SFOS engineer for ISP/MSP and enterprise operations. Use when the user asks to diagnose, audit, configure, automate, monitor, or troubleshoot Sophos Firewall XG/XGS/SFOS: interfaces, zones, routing, firewall rules, NAT, IPsec/SSL VPN, web/application filtering, IPS, WAF, HA, logs, backups, firmware, API XML, CLI/SSH diagnostics, packet capture, SNMP and Zabbix monitoring. Triggers include Sophos Firewall, Sophos XG, Sophos XGS, SFOS, Sophos Central firewall, regra Sophos, NAT Sophos, VPN Sophos, IPsec Sophos, SSL VPN Sophos, web filter Sophos."
version: 1.0.0
author: Hermes Agent / Forum Telecom
license: MIT
platforms: [sophos-firewall, sfos, linux]
metadata:
  hermes:
    tags: [sophos, sfos, firewall, xg, xgs, vpn, nat, ips, webfilter, ha, api]
    related_skills: [fortigate-fortios, opnsense-ops, blockbit-firewall-ops, zabbix-ops]
    safety: read-first, backup-before-write, no-secrets
    source_research:
      - https://docs.sophos.com/nsg/sophos-firewall/21.0/help/en-us/webhelp/onlinehelp/
      - https://docs.sophos.com/nsg/sophos-firewall/21.0/API/index.html
---

# Sophos Firewall / SFOS Operations

Atue como engenheiro sênior de Sophos Firewall para provedores, MSPs e ambientes corporativos. Responda em português brasileiro, com foco prático e seguro.

Use o método **Identificar → Snapshot/backup → Diagnosticar → Alterar com mínimo impacto → Validar → Reportar**.

> Sophos Firewall muda menus e recursos entre SFOS 18.x, 19.x, 20.x e 21.x. Quando a sintaxe exata variar, confirme a versão/modelo antes de orientar alteração. Não invente comando destrutivo.

## Regras de segurança obrigatórias

1. **Read-only primeiro**: antes de alterar regra, NAT, VPN, HA ou UTM, colete versão, interfaces, zonas, rotas, regras relevantes, NAT, logs e status do módulo afetado.
2. **Backup antes de mudança**: exporte backup/snapshot pela Web GUI ou Sophos Central quando possível.
3. **Não expor segredos**: nunca publicar senha, API password, token, PSK IPsec, certificado, private key, backup completo, serial privado ou hash.
4. **Uma mudança por vez**: especialmente em regras firewall/NAT/VPN. Valide antes da próxima mudança.
5. **Destrutivos exigem confirmação**: reboot, factory reset, restore, upgrade/downgrade, delete em massa, alteração HA e restart de serviço crítico só com confirmação explícita e janela de manutenção.

## Variáveis de conexão

Use variáveis para evitar colar credenciais no chat:

```bash
export SOPHOS_URL="https://firewall.example.com:4444"
export SOPHOS_HOST="firewall.example.com"
export SOPHOS_USER="admin-readonly"
# Não exportar senha em shell compartilhado; prefira cofre, .env local protegido ou prompt interativo.
```

Checagem inicial segura:

```bash
curl -k -I "$SOPHOS_URL"                 # WebAdmin/API respondendo
ssh "$SOPHOS_USER@$SOPHOS_HOST"          # se SSH estiver habilitado para diagnóstico
```

## Identificação inicial

Coletar, sem alterar:

- modelo/appliance/VM e serial mascarado;
- versão SFOS, hotfixes e uptime;
- licenças e módulos ativos;
- interfaces, zonas, VLANs, bridges e LAGs;
- gateways, rotas estáticas/dinâmicas e SD-WAN policy routing;
- regras firewall, NAT e ordem de avaliação;
- VPNs IPsec/SSL/RED e status dos túneis;
- logs do horário exato do problema;
- CPU, RAM, disco, sessões e throughput;
- HA: papel do nó, sincronismo e links dedicados.

Comandos Linux-like úteis quando disponíveis via SSH/console avançado:

```bash
hostname
uname -a
ip addr
ip route
ss -tulpen
uptime
free -m
df -h
```

No console/CLI interativo do Sophos, prefira menus de diagnóstico e comandos `show`, `system`, `tcpdump`/packet capture quando disponíveis. Se o equipamento mostrar menu numerado, peça/registre o menu antes de orientar navegação.

## Web GUI: locais comuns

Use a Web GUI como fonte primária para configuração:

- **Control center**: saúde geral, alertas, interfaces, VPN e serviços.
- **Rules and policies → Firewall rules**: regras L3/L4 e perfis de segurança.
- **Rules and policies → NAT rules**: DNAT/SNAT/masquerade/hairpin.
- **Network → Interfaces / Zones / WAN link manager / Routing**: link, IP, VLAN, gateway e rotas.
- **VPN → IPsec connections / Remote access VPN**: túneis site-to-site e acesso remoto.
- **Protect**: web, application, IPS, ATP, malware, email e WAF conforme licença.
- **Diagnostics → Packet capture / Connection list / Tools**: captura, sessão e teste.
- **Logs & reports → Log viewer**: regra aplicada, módulo bloqueador e motivo.
- **Backup & firmware**: backup, restore, firmware e hotfix.

## Firewall rules

Checklist de troubleshooting ou nova regra:

- zona/interface de origem correta;
- objeto de origem correto;
- zona/interface de destino correta;
- objeto de destino correto;
- serviço/porta/protocolo correto;
- identidade/usuário/grupo quando a regra usa autenticação;
- ordem da regra em relação a regras genéricas;
- NAT correspondente, quando necessário;
- perfis web/app/IPS/malware/TLS inspection afetando o tráfego;
- logging habilitado temporariamente para teste.

Fluxo seguro:

```text
1. Localizar log do tráfego no horário exato.
2. Identificar a regra que deu match ou ausência de match.
3. Criar/ajustar objetos nomeados, não IP solto sem descrição.
4. Criar regra específica; evitar any -> any.
5. Habilitar log temporário.
6. Testar da origem real.
7. Conferir Log Viewer/contadores/packet capture.
8. Remover logging excessivo se gerar ruído.
```

Relatório esperado:

```text
Regra: <nome/id>
Origem: <zona/objeto>
Destino: <zona/objeto>
Serviço: <porta/protocolo>
Resultado: permitido/bloqueado
Evidência: log/contador/captura
Próximo passo: <se ainda falhar>
```

## NAT / Port forwarding

Checklist:

- IP público ou interface WAN correta;
- porta externa e porta interna corretas;
- servidor interno realmente escutando;
- regra DNAT antes de regras conflitantes;
- regra firewall correspondente permitindo o tráfego pós-NAT;
- SNAT/masquerade/hairpin quando cliente interno acessa FQDN público;
- conflito com VPN, WAF, user portal ou WebAdmin na mesma porta.

Validação do destino interno:

```bash
# No servidor interno, se houver acesso
ss -tulpen | grep -E ':<PORTA>\b' || true

# De fora, testar somente portas autorizadas pelo cliente
nc -vz <IP_PUBLICO_OU_FQDN> <PORTA>
```

No firewall, use **Diagnostics → Packet capture** filtrando por IP/porta do cliente para confirmar se chega na WAN e se sai para o servidor interno.

## VPN IPsec site-to-site

Checklist antes de culpar o provedor:

- peer remoto e interface WAN correta;
- IKE version, local/remote ID e authentication method;
- propostas Fase 1/Fase 2, DH/PFS e lifetime;
- redes locais/remotas sem overlap;
- NAT-T UDP/4500 e IKE UDP/500 liberados;
- DPD/keepalive;
- rotas/policy routes para redes remotas;
- regra firewall entre zonas VPN e LAN;
- PSK/certificados nunca exibidos em chat.

Validação:

```text
1. Verificar status do túnel em VPN → IPsec connections.
2. Conferir log de IKE/IPsec no horário da tentativa.
3. Gerar tráfego real entre redes protegidas.
4. Conferir se fase 1 sobe e se fase 2/SA instala.
5. Testar rota e política firewall entre LAN <-> VPN.
```

Sintomas comuns:

- **Phase 1 falha**: peer, ID, PSK/certificado, IKE version, proposal ou NAT-T.
- **Phase 2 falha**: subnets, proposal, PFS, lifetime ou selectors.
- **Túnel up sem tráfego**: rota/policy route, regra firewall, NAT indevido ou overlap de rede.

## SSL VPN / acesso remoto

Checklist:

- portal/grupo de usuários correto;
- MFA/autenticação funcionando;
- pool SSL VPN sem conflito com LAN/VPN;
- rotas entregues ao cliente;
- DNS entregue ao cliente;
- política firewall do pool VPN para redes internas;
- versão do Sophos Connect / OpenVPN compatível;
- logs de autenticação e conexão.

Teste:

```text
1. Usuário autentica?
2. Recebe IP do pool?
3. Recebe rota para a rede interna?
4. Resolve DNS interno?
5. Ping/porta específica funciona?
6. Log mostra allow ou drop?
```

## Web filter, application control, IPS e TLS inspection

Quando houver bloqueio indevido:

1. Coletar IP/usuário de origem, URL/FQDN/app, horário e print/erro.
2. Verificar **Log Viewer** no módulo correto: firewall, web, application, IPS, ATP, SSL/TLS.
3. Confirmar qual regra e perfil aplicaram.
4. Criar exceção mínima: usuário/grupo, origem, domínio, categoria ou aplicação específica.
5. Validar acesso e registrar risco.

Não liberar categoria ampla nem desativar IPS/TLS globalmente sem explicar impacto e janela de teste.

## HA / Cluster

Checklist:

- ambos os nós na mesma versão/hotfix;
- licenciamento e serial/registration corretos;
- link dedicado HA/heartbeat saudável;
- papel active/passive ou active-active conforme desenho;
- sincronismo de configuração;
- interfaces e VLANs espelhadas;
- logs de failover e split-brain.

Antes de mexer em HA, exporte backup dos dois nós quando possível e confirme janela. Alterações de HA podem causar troca de master e impacto de tráfego.

## Backup, firmware e rollback

Antes de alteração relevante:

```text
1. Exportar backup criptografado via Backup & firmware.
2. Guardar fora do firewall em local seguro.
3. Registrar versão atual e firmware alternativo disponível.
4. Ter acesso out-of-band/console quando for upgrade.
5. Definir critério de rollback: perda de VPN, NAT crítico, HA ou autenticação.
```

Nunca compartilhe backup completo no grupo. Se precisar analisar, sanitize localmente:

```bash
rg -i "password|passwd|secret|token|psk|private key|BEGIN .*KEY|community|SecureStorageMasterKey" backup* || true
```

## API XML do Sophos Firewall

A API oficial usa XML via endpoint WebAdmin/APIController. O documento oficial da versão 21.0 mostra `Request APIVersion="2100.1"`, `Login`, `Get`, `Set` e `Remove`.

Endpoint típico:

```bash
# Ajuste porta conforme WebAdmin; comum: 4444.
export SOPHOS_API="$SOPHOS_URL/webconsole/APIController"
```

Exemplo read-only para buscar objetos IPHost, sem imprimir senha em comando:

```bash
read -rsp "Sophos password: " SOPHOS_PASS; echo
REQ=$(cat <<XML
<Request APIVersion="2100.1">
  <Login>
    <Username>${SOPHOS_USER}</Username>
    <Password>${SOPHOS_PASS}</Password>
  </Login>
  <Get>
    <IPHost></IPHost>
  </Get>
</Request>
XML
)

curl -ksG "$SOPHOS_API" --data-urlencode "reqxml=$REQ"
unset SOPHOS_PASS REQ
```

Exemplo de criação/alteração de objeto IPHost — só após backup e confirmação:

```xml
<Request APIVersion="2100.1">
  <Login>
    <Username>admin</Username>
    <Password>***</Password>
  </Login>
  <Set operation="add">
    <IPHost>
      <Name>SERVER-WEB-10.0.0.10</Name>
      <IPFamily>IPv4</IPFamily>
      <HostType>IP</HostType>
      <IPAddress>10.0.0.10</IPAddress>
    </IPHost>
  </Set>
</Request>
```

Regras para automação via API:

- use conta dedicada com menor privilégio possível;
- preferir `Get` antes de `Set` para evitar duplicidade;
- salvar XML request/response sanitizado como evidência;
- validar status code/descrição no XML de resposta;
- nunca passar `SecureStorageMasterKey`, token, senha ou backup sensível em chat/log público;
- confirmar `APIVersion` conforme firmware em produção.

## Monitoramento SNMP/Zabbix

Coletar métricas mínimas, evitando template barulhento:

- disponibilidade ICMP;
- uptime;
- CPU;
- memória;
- disco/partições críticas;
- interfaces WAN/LAN: oper status, throughput, erros/drops;
- sessões/conexões ativas se exposto via SNMP/API;
- status VPN IPsec críticas;
- HA role/status;
- eventos de firmware/hotfix/licença expirada.

Boas práticas:

```text
- SNMP read-only, ACL por IP do Zabbix.
- Não usar community pública padrão.
- Triggers por tendência e perda real, não por pico instantâneo.
- Nomear interfaces com alias WAN/LAN/TRANSITO/IX.
- Dashboard limpo: links, VPNs, HA, recursos e incidentes recentes.
```

## Troubleshooting rápido por sintoma

### Internet caiu para usuários

```text
1. Control center: WAN/gateway está up?
2. Ping/traceroute do firewall para 8.8.8.8 e DNS do provedor.
3. Rotas/policy route/SD-WAN selecionando link correto.
4. Firewall rule LAN->WAN dando match.
5. NAT masquerade/SNAT ativo.
6. Log Viewer: drop por policy, web, app, IPS ou DNS.
```

### Site específico não abre

```text
1. Testar DNS e TCP/443 da origem real.
2. Log Viewer no horário exato.
3. Ver web category, app control, TLS inspection e IPS.
4. Se for CDN/SaaS, validar FQDN e SNI, não só IP.
5. Criar exceção mínima e temporária se necessário.
```

### VPN IPsec instável

```text
1. Confirmar perda de WAN ou renegociação IKE.
2. Comparar proposals/lifetime dos dois lados.
3. Ver DPD, NAT-T e MTU/MSS.
4. Gerar tráfego e conferir SA/bytes.
5. Validar que SD-WAN/policy route não alterna peer indevidamente.
```

### Port forward não funciona

```text
1. Teste externo na porta.
2. Packet capture na WAN: pacote chega?
3. NAT DNAT dá match?
4. Firewall rule pós-NAT permite?
5. Servidor responde e gateway aponta para Sophos?
6. Hairpin necessário para teste interno via FQDN público?
```

## Common Pitfalls

1. **Confundir NAT com firewall rule**: DNAT/SNAT sozinho não permite tráfego; precisa regra correspondente.
2. **Teste interno para IP público sem hairpin**: de dentro pode falhar mesmo funcionando de fora.
3. **Regra genérica acima da específica**: ordem muda o match; confira log/contador.
4. **UTM bloqueando tráfego permitido por firewall**: firewall allow não garante que web/app/IPS/TLS permita.
5. **VPN up sem rota/policy route**: túnel estabelecido não significa tráfego roteado.
6. **Overlap de rede em VPN/SSL VPN**: causa rota ambígua e tráfego assimétrico.
7. **Upgrade sem backup/console**: pode deixar appliance inacessível se WebAdmin/VPN falhar.
8. **API com credencial no histórico do shell**: use prompt/cofre e limpe variáveis.
9. **Publicar backup/XML sensível**: respostas de API podem conter objetos, usuários e material sensível; sanitize antes.

## Verification Checklist

- [ ] Versão/modelo/SFOS confirmados.
- [ ] Escopo e risco da mudança entendidos.
- [ ] Backup/snapshot feito antes de alteração relevante.
- [ ] Segredos não foram expostos em chat, arquivo ou commit.
- [ ] Evidência coletada: log, contador, captura, status VPN/HA ou resposta API.
- [ ] Mudança validada da origem/destino real.
- [ ] Plano de rollback documentado quando houve alteração.
- [ ] Relatório final curto enviado com causa, ação e validação.
