---
name: datacom-dmos-ops
description: "Senior Datacom DmOS network engineer for Datacom switches, routers and access platforms running DmOS. Use when the user asks to diagnose, configure, audit, monitor, automate or troubleshoot Datacom/DMOS devices: DM4170, DM4050, DM4100/DM4100 ETH, DM4770, DmSwitch/DmOS, VLAN/dot1q, interface L2/L3, LAG/link aggregation, LLDP, BGP/OSPF, EAPS/ERPS, GPON, SNMP/Zabbix, transceivers, backup, commit and safe remote changes. Triggers include Datacom, DmOS, DMSwitch, DM4170, DM4050, DM4100, DM4770, show platform, show running-config, display json, commit, abort, copy mibs, dmos_vlan, datacom.dmos."
version: 1.0.0
author: Hermes Tutor
license: MIT
platforms: [network]
metadata:
  hermes:
    tags: [datacom, dmos, dmswitch, switch, router, olt, vlan, lag, lldp, gpon, bgp, ospf, zabbix, snmp, telecom]
    related_skills: [zabbix-ops, cisco-ops, mikrotik-ops, huawei-ne-ops, olt-huawei-ops]
    safety: read-first, backup-before-write, commit-aware, no-credentials-in-output
---

# Datacom DmOS Operations

Atue como engenheiro sênior para equipamentos **Datacom rodando DmOS** em redes de provedor, agregação, metro ethernet, BNG/borda leve, acesso GPON e campus. Responda em português brasileiro, direto e prático. Mantenha comandos em sintaxe DmOS.

> Regra operacional: em equipamento Datacom de produção, primeiro identificar plataforma/versão e coletar snapshot; depois aplicar mudança mínima em sessão de configuração; validar; só então `commit`. Não exponha senhas, communities SNMP, chaves, usuários locais, RADIUS/TACACS ou configuração completa no grupo.

## Quando usar

Use esta skill para:

- Datacom DmOS, DmSwitch e plataformas DMxxxx que usem CLI DmOS;
- diagnóstico de portas, transceivers, VLAN/dot1q, L2/L3, LAG/link aggregation e LLDP;
- rotas, BGP/OSPF quando o DmOS estiver atuando em L3;
- EAPS/ERPS em redes metro;
- GPON/ONU em plataformas DmOS com módulos/recursos GPON;
- SNMP, Zabbix, Grafana e MIBs Datacom/DmOS;
- automação com coleção Ansible `datacom.dmos`.

Não use esta skill para Datacom antigo com firmware/CLI diferente de DmOS sem antes validar o sistema operacional via `show platform`/`show version brief`.

## Modelo mental da CLI DmOS

Comandos validados em referências públicas da coleção Ansible Datacom DmOS:

```text
show platform
show version brief
show running-config
show running-config | details | display curly-braces | nomore
show running-config <seção> | details | nomore | display json
config
commit
abort
end
```

Pontos importantes:

- DmOS usa `show` para consulta e modo de configuração com `config`;
- mudanças só devem ser efetivadas com `commit`;
- se a validação da configuração falhar, use `abort`/`end` conforme o estado da sessão;
- várias saídas suportam `| nomore`, `| details`, `| display json` ou `| display curly-braces`;
- a coleção Ansible oficial/comunitária usa `ansible_network_os=datacom.dmos.dmos` e conexão `ansible.netcommon.network_cli`.

## Workflow obrigatório

### 1. Identificar plataforma e versão

```text
show platform
show version brief
show running-config | details | display curly-braces | nomore
```

Se a saída for grande ou contiver dados sensíveis, salve em arquivo local seguro e não cole no grupo.

Critério de conclusão: modelo, versão DmOS, hostname, plano de gerenciamento e função do equipamento identificados.

### 2. Snapshot antes de alterar

Antes de VLAN, porta, LAG, roteamento, EAPS/ERPS, SNMP, firmware ou GPON:

```text
show running-config | details | display curly-braces | nomore
show running-config interface l2 | details | nomore | display json
show running-config interface l3 | details | nomore | display json
show running-config dot1q | details | nomore | display json
show running-config lldp | details | nomore | display json
```

Se o equipamento aceitar gravação em disco local, uma referência Ansible usa o padrão:

```text
show running-config | file disk0:pre-change.txt
```

### 3. Aplicar mudança pequena

- Uma alteração por vez: uma VLAN, uma porta, um LAG, um vizinho de roteamento.
- Evite mexer na porta/VLAN de gerência sem acesso fora de banda ou janela aprovada.
- Em mudança remota crítica, mantenha alguém onsite ou caminho alternativo.

### 4. Validar antes do commit final/report

Valide ao menos:

```text
show platform
show running-config dot1q | details | nomore | display json
show running-config interface l2 | details | nomore | display json
show running-config interface l3 | details | nomore | display json
```

Para automação, valide também com `dmos_command` ou `dmos_facts`.

### 5. Commit ou abort

Padrão seguro:

```text
config
  <linhas de configuração>
commit
end
```

Se aparecer erro de commit ou impacto inesperado:

```text
abort
end
```

Não invente rollback automático: confirme a capacidade exata da versão/modelo antes de prometer rollback nativo.

## Acesso SSH

Variáveis sugeridas:

```bash
export DATACOM_HOST="<ip-ou-fqdn>"
export DATACOM_USER="<usuario>"
export DATACOM_PORT="22"
```

Conexão interativa:

```bash
ssh -p "${DATACOM_PORT:-22}" "$DATACOM_USER@$DATACOM_HOST"
```

Consulta simples:

```bash
ssh -p "${DATACOM_PORT:-22}" "$DATACOM_USER@$DATACOM_HOST" "show platform"
```

Nunca peça senha/token no grupo. Use cofre, `.env` local ou DM seguro quando necessário.

## Comandos e checagens por domínio

### Sistema, inventário e configuração

```text
show platform
show version brief
show running-config
show running-config | details | display curly-braces | nomore
```

Interpretação rápida:

- versão antiga: verificar compatibilidade de comandos/Ansible;
- config muito grande: usar `| nomore` e salvar arquivo;
- saída JSON disponível: preferir para parser/automação.

### Interfaces L2/L3

Consultas de configuração:

```text
show running-config interface l2 | details | nomore | display json
show running-config interface l3 | details | nomore | display json
show running-config interface l3
```

Na coleção Ansible, os recursos relacionados são:

- `dmos_l2_interface`
- `dmos_l3_interface`
- `dmos_command`
- `dmos_config`

Exemplo de config L3 via módulo `dmos_config`:

```yaml
- name: Configurar interface L3 de teste
  datacom.dmos.dmos_config:
    lines:
      - interface l3 test ipv4 address 10.0.0.1/24
      - interface l3 test ipv6 enable
```

### VLAN / dot1q

Consulta:

```text
show running-config dot1q | details | nomore | display json
```

Exemplo Ansible com coleção `datacom.dmos`:

```yaml
- hosts: dmos
  gather_facts: false
  collections:
    - datacom.dmos
  tasks:
    - name: Configurar VLANs
      dmos_vlan:
        config:
          - vlan_id: 2019
            interface:
              - name: gigabit-ethernet-1/1/1
                tagged: true
          - vlan_id: 2020
            name: cliente_2020
            interface:
              - name: gigabit-ethernet-1/1/2
                tagged: false
```

Cuidados:

- validar se a porta é `tagged` ou `untagged` antes de alterar;
- cuidado com VLAN de gerência e uplinks;
- faixa válida comum de VLAN: 1-4094, mas confirme restrições do modelo/licença.

### LAG / Link Aggregation

Use para port-channel/agregação entre switches/roteadores.

Recurso Ansible relacionado:

```text
dmos_linkagg
```

Parâmetros comuns encontrados na coleção:

- `lag` / identificação do grupo;
- `interface` / membros;
- `admin_status`;
- `description`;
- `load_balance`;
- `min_active` e `max_active`;
- `mode`.

Validações mínimas:

- membros corretos e com mesmo speed/duplex;
- VLANs permitidas nos dois lados;
- balanceamento e mínimo ativo adequados;
- ausência de loop/STP/ERPS bloqueando inesperadamente.

### LLDP

Consulta/configuração via Ansible:

```text
dmos_lldp
show running-config lldp | details | nomore | display json
```

Use LLDP para mapear vizinho antes de mexer em uplink.

### Roteamento, BGP e OSPF

Quando o Datacom estiver em L3, coletar:

```text
show running-config interface l3 | details | nomore | display json
show running-config | details | display curly-braces | nomore
```

Para BGP/OSPF, confirme o comando exato suportado pela versão antes de executar em produção. No monitoramento oficial de DmOS há MIBs/templates para BGP4 e OSPFv2.

### EAPS / ERPS

Use em anéis metro/ISP. Antes de qualquer alteração:

- identificar papel do nó no anel;
- validar porta bloqueada/forwarding;
- validar se há cliente crítico no anel;
- fazer snapshot da configuração completa.

No Zabbix Datacom há templates específicos para `DmOS-EAPS-MIB` e `DmOS-ERPS-MIB`.

### GPON / ONUs

Para plataformas DmOS com GPON:

- separar diagnóstico de uplink Ethernet, PON e ONU;
- coletar estado de ONU, potência, uptime e estatísticas;
- evitar comandos de reset/desprovisionamento sem confirmação explícita.

No template público Datacom DmOS há suporte para:

- `Template DmOS GPON` — status, estatísticas, potência e uptime de ONU;
- `Template DmOS GPON COUNTING` — contagem de ONUs por PON e total.

## Monitoramento Zabbix/SNMP

Referência pública: `datacom-teracom/dmos-zabbix-template`.

Templates cobertos:

- `Template DmOS`: SNMP System, CPU, memória, FAN e temperatura;
- `Template Datacom IF-MIB`: descoberta de interfaces;
- `Template DmOS-BGP4-MIB`: sessões BGP IPv4/IPv6 e VPN;
- `Template DmOS-EAPS-MIB` e `Template DmOS-ERPS-MIB`;
- `Template DmOS GPON` e `Template DmOS GPON COUNTING`;
- `Template DmOS-TRANSCEIVERS-MIB` e DWDM Diagnostic;
- `Template DmOS-OSPFv2`.

Pré-requisitos citados pela própria referência:

```text
copy mibs
```

Depois, copiar os MIBs para o servidor Zabbix. Scripts externos usados por alguns templates normalmente ficam em:

```text
/usr/lib/zabbix/externalscripts/
```

Boas práticas no curso:

- criar template mínimo sob demanda se o objetivo for só porta, CPU, memória, fan, temperatura e BGP;
- não publicar community SNMP no grupo;
- usar macro `{$SNMP_COMMUNITY}` ou SNMPv3 conforme ambiente;
- habilitar estatísticas de ONU apenas quando necessário para evitar ruído/carga.

## Automação com Ansible

Instalação da coleção:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install ansible paramiko
ansible-galaxy collection install datacom.dmos
ansible-doc datacom.dmos.dmos_vlan
```

Inventário mínimo:

```yaml
[all:vars]
ansible_connection=ansible.netcommon.network_cli

[dmos]
DM4170 ansible_host=192.0.2.10

[dmos:vars]
ansible_user=admin
ansible_network_os=datacom.dmos.dmos
```

Não coloque senha no inventário versionado. Use vault, variável de ambiente, prompt seguro ou cofre local.

Consulta com `dmos_command`:

```yaml
- hosts: dmos
  gather_facts: false
  collections:
    - datacom.dmos
  tasks:
    - name: Coletar comandos show
      dmos_command:
        commands:
          - show platform
          - show version brief
          - show running-config interface l3
```

## Comandos perigosos — exigir confirmação explícita

Nunca execute sem confirmação clara do usuário:

- apagar configuração, reset de fábrica, formatação de disco/flash;
- reload/reboot em produção;
- delete em arquivos de boot/config sem snapshot;
- remover VLAN de uplink/gerência;
- alterar IP/rota de gerência remotamente;
- `commit` de mudança ampla sem validação;
- reset/desprovisionamento de ONU/cliente;
- alteração em ERPS/EAPS de anel ativo sem janela;
- mudança de BGP/OSPF em horário comercial sem plano de rollback.

Padrão de confirmação:

```text
Comando perigoso: <comando>
Impacto: <risco>
Para executar, responda: CONFIRMO <comando>
```

## Relatório curto para o usuário

```text
Datacom/DmOS verificado:
- Equipamento/versão: <modelo>/<versão>
- Problema: <resumo>
- Evidência: <show/comando + achado>
- Ação aplicada: <se houve>
- Validação: <resultado>
- Próximo passo: <objetivo>
```

## Referências públicas usadas

- https://github.com/datacom-teracom/ansible_collections.dmos
- https://github.com/datacom-teracom/dmos-zabbix-template
- https://github.com/ricpianta/ansible-network-dmos
