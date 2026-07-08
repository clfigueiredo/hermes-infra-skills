# Hermes Infra Skills - ForumTelecom

Backup versionado das skills de infraestrutura usadas pelo Hermes Agent.

## Conteúdo

- `forumtelecom/`: skills de operação de infraestrutura/telecom
  - MikroTik
  - Zabbix
  - Proxmox
  - Docker
  - Cisco
  - Huawei NE
  - OLT Huawei
  - OLT FiberHome
  - OPNsense
  - VMware
  - Hyper-V

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
