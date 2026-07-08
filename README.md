# Hermes Infra Skills - ForumTelecom

Backup versionado das skills de infraestrutura usadas pelo Hermes Agent.

## Conteúdo

- `forumtelecom/`: skills de operação de infraestrutura/telecom
  - MikroTik
  - Zabbix
  - Proxmox
  - Docker
  - Cisco
  - Cisco Catalyst switches
  - Huawei NE
  - Switch Huawei S6730/S6720
  - OLT Huawei
  - OLT FiberHome
  - OPNsense
  - VMware
  - Hyper-V
  - FortiGate / FortiOS
  - OLT VSOL
  - OLT ZTE C300/C320
  - OLT Intelbras EPON / OLT 4840 E
  - Firewall Blockbit
  - Agenda / calendário / lembretes
  - Financeiro administrativo
  - Sophos Firewall / SFOS
  - TRENDnet switches
  - Ubiquiti airMAX AC/M5
  - Datacom DmOS
  - Mimosa C5c/C5x/B5/A5 wireless

## Restaurar em outro Hermes

A partir da raiz deste repositório:

```bash
mkdir -p /root/.hermes/skills
cp -a .hermes/skills/forumtelecom /root/.hermes/skills/
```

Depois, no Hermes:

```text
/reload-skills
```

ou reinicie o gateway/sessão.

## Verificação

```bash
find .hermes/skills/forumtelecom -name 'SKILL.md' -print
```
