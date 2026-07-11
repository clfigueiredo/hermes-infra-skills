# Hermes Infra Skills - ForumTelecom

Backup versionado das skills de infraestrutura usadas pelo Hermes Agent.

## Conteúdo

- `forumtelecom/`: skills de operação de infraestrutura/telecom
- `curso-hermes/`: skills gerais para alunos do Hermes Agent, vibe coding, desenvolvimento, revisão, segurança e produtividade
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
  - Atendimento ISP N1/N2 via WhatsApp
  - TR-069 / ACS / GenieACS
  - Desenvolvimento web / sites premium
  - EVE-NG / UNetLab
  - Active Directory / Windows File Server
  - SGP Provedor / API ERP ISP

## Restaurar em outro Hermes

A partir da raiz deste repositório:

```bash
mkdir -p ~/.hermes/skills
cp -a .hermes/skills/forumtelecom ~/.hermes/skills/
cp -a .hermes/skills/curso-hermes ~/.hermes/skills/
```

Para instalar só as skills de alunos:

```bash
mkdir -p ~/.hermes/skills
cp -a .hermes/skills/curso-hermes ~/.hermes/skills/
```

Depois, no Hermes:

```text
/reload-skills
```

ou reinicie o gateway/sessão.

## Catálogo de skills

Página visual para alunos, com cards, exemplos e comandos de instalação:

- [docs/index.html](docs/index.html)
- [docs/sgp-api-capabilities.html](docs/sgp-api-capabilities.html): mapa objetivo da API SGP analisada a partir da coleção Postman

## MCP servers

- [mcp/sgp-api-mcp](mcp/sgp-api-mcp): MCP server para integração segura com SGP Provedor/API ERP ISP

Catálogo Markdown completo com explicação, uso e comando de acionamento de cada skill:

- [SKILLS-CATALOG.md](SKILLS-CATALOG.md)

## Verificação

```bash
find .hermes/skills -name 'SKILL.md' -print
```
