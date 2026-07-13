---
name: beesweb-isp-ops
description: "Use when operating, integrating, or supporting Beesweb/BeesWeb ISP management system for providers: customer registration, contracts, PPPoE/Hotspot authentications, MikroTik/server integration, OLT/ONU authorization, CTO mapping, financial billing, customer release by observation, tickets/work orders, logs/auditing, WhatsApp/Hermes pre-attendance and safe read-only API/browser workflows."
version: 1.0.0
author: Hermes Tutor
license: MIT
metadata:
  hermes:
    tags: [beesweb, beesweb-isp, erp, provedor, isp, atendimento, financeiro, contratos, pppoe, mikrotik, olt, cto, chamados]
    related_skills: [atendimento-isp-n1-n2, dashboard-noc-diagnostico-cliente, sgp-api-integration-ops, mikrotik-ops, olt-huawei-ops, olt-fiberhome-ops, olt-intelbras-epon-ops, olt-vsol-ops, olt-zte-c300-ops]
    safety: read-first, no-credentials-in-chat, least-privilege, human-approval-for-write
---

# Beesweb ISP Operations

## Visão geral

Use esta skill quando o usuário pedir ajuda com **Beesweb/BeesWeb**, sistema de gestão para provedores, incluindo atendimento, cadastro de clientes, contratos, autenticações PPPoE/Hotspot, financeiro, chamados, integração com servidores MikroTik/RB, integração com OLTs, CTOs e auditoria.

Referências públicas consultadas:

- Painel admin: `https://app.beesweb.com.br/auth/login`
- Central do cliente: `https://adm.beesweb.com.br/login`
- Helpdesk: `https://beesweb.crisp.help/pt-br/`
- App Android BeesWeb Painel: `br.com.beesweb.adm`

> Importante: não foi localizada documentação pública oficial de API REST do Beesweb durante a criação desta skill. Para automação em produção, priorize API/documentação enviada pelo fornecedor ou integração autorizada. Sem API documentada, trate uso via browser como operação assistida e com aprovação humana para escrita.

## Postura operacional obrigatória

1. **Read-only primeiro**: consultar cliente, contrato, financeiro, autenticação, logs e chamado antes de qualquer alteração.
2. **Não pedir nem expor senhas**: não solicitar senha de cliente, senha PPPoE, senha de painel, token, cookie, sessão Web ou credenciais de RB/OLT no grupo.
3. **Permissão mínima**: usar usuário Beesweb com perfil limitado para laboratório e integrações read-only quando disponível.
4. **Escrita com aprovação**: liberar cliente, criar boleto, editar contrato, criar autenticação, conectar servidor, autorizar ONU ou abrir/fechar chamado só com regra clara e confirmação do operador.
5. **Auditoria**: registrar técnico, cliente/contrato mascarado, ação, horário e evidência.
6. **Não alterar produção no escuro**: mudanças em servidor, OLT, planos, financeiro e contratos exigem validação e janela quando impactarem serviço.

## Módulos e caminhos úteis

### Clientes

Helpdesk indica operações em `Clientes`:

- `Clientes > Todos`: cadastro/listagem/ativação/desativação de clientes.
- `Clientes > Autenticações`: cadastro e gestão de autenticações PPPoE/Hotspot.
- `Clientes > Contratos`: contratos vinculados ao cliente.
- Cadastro pode incluir dados do titular, endereço, contrato, autenticação e dados complementares.

Artigos de referência:

- `Como cadastrar um novo cliente`
- `Cadastro de Autenticação`
- `Listagem de Cliente`
- `Como Ativar e Desativar Cliente`
- `É possível ter mais de um login por cliente?`

### Contratos

Caminho público citado:

```text
Clientes > Contratos
Contrato > Todos
```

Uso comum:

- criar/editar contrato;
- associar plano;
- imprimir/assinar contrato;
- liberar cliente pelo contrato;
- ativar mensagem de pendência ou bloqueio;
- edição em lote com cuidado.

### Autenticações PPPoE/Hotspot

Caminho:

```text
Clientes > Autenticações
```

Campos citados pela documentação:

- tipo: PPPoE, Hotspot ou ambos;
- login e senha;
- servidor integrado;
- plano;
- IP/MAC para fixação quando aplicável;
- tags;
- status ativo/inativo;
- opções adicionais de Wi-Fi.

Boas práticas:

- evitar caracteres especiais em secrets/profiles durante importações, conforme alerta do helpdesk;
- nunca expor senha PPPoE no WhatsApp/grupo;
- confirmar se servidor/plano existem e estão sincronizados antes de criar login.

### Rede / Servidores MikroTik

Caminho:

```text
Rede > Servidores
```

Pontos públicos do Beesweb:

- cada servidor criado tem **script próprio de conexão**;
- não reutilizar script de um servidor em outro;
- porta API MikroTik citada: `8728`;
- recomendação pública: usar VPN;
- sem VPN, o IP precisa ser público/direcionado;
- para conexão funcionar, o servidor precisa ter DNS configurado e ping para rede externa.

Fluxo seguro para conectar servidor:

1. Criar servidor no Beesweb.
2. Copiar o script gerado pelo próprio servidor.
3. Colar no terminal do MikroTik/RB correspondente.
4. Validar status em `Rede > Servidores`.
5. Se logs não aparecem, exportar configurações do servidor e validar logs na RB.

Nunca publicar script de conexão no grupo: pode conter credenciais, endereços e comandos sensíveis.

### Sincronização sistema ↔ servidor

A documentação cita duas direções:

```text
Servidor -> Beesweb: importar logins, planos e pools do MikroTik/RB para o sistema.
Beesweb -> Servidor: exportar logins, planos e pools do sistema para o MikroTik/RB.
```

Uso típico:

- novo servidor entrando no Beesweb;
- backup/migração de RB;
- reconstrução de servidor;
- migração de clientes entre servidores.

Cuidados:

- fazer backup da RB antes;
- validar profiles/secrets/pools;
- testar em poucos clientes antes de lote;
- evitar caracteres especiais em profiles/secrets durante importação;
- não executar importação/exportação em massa sem aprovação.

### OLT / ONU

Caminho:

```text
Rede > OLTs
```

O helpdesk público informa módulo de OLT para autorização de ONU. Fabricantes citados:

```text
Huawei, FiberHome, ZTE, Cianet, PARKS, Intelbras, CDATA, TP-Link, Datacom, VSOL, Digistar
```

Campos citados:

- nome da OLT;
- IP público/direcionado;
- porta Telnet ou porta redirecionada;
- login;
- senha;
- fabricante.

Cuidados:

- não deixar Telnet aberto diretamente na internet quando possível; preferir VPN/ACL/port forwarding controlado;
- criar usuário específico para o painel, com permissão necessária e auditável;
- não colar senha/login de OLT no grupo;
- carregar skill específica do fabricante para diagnóstico profundo.

Skills relacionadas:

- `olt-huawei-ops`
- `olt-fiberhome-ops`
- `olt-zte-c300-ops`
- `olt-intelbras-epon-ops`
- `olt-vsol-ops`

### CTO

Caminho:

```text
Rede > CTO > + Novo CTO
```

Uso:

- cadastrar CTO;
- informar identificação/endereço;
- associar login/cliente a porta;
- evitar associar o mesmo login em mais de uma CTO;
- verificar ocupação/disponibilidade das portas.

Bom uso com Hermes:

- consultar cliente/contrato/login;
- validar CTO/porta antes de deslocar técnico;
- anexar CTO/porta no chamado/OS;
- sugerir porta livre para instalação quando a integração permitir.

### Financeiro

Módulo financeiro cobre:

- boletos/cobranças;
- carnês;
- relatórios financeiros;
- descontos;
- cobrança proporcional;
- liberação por observação/confiança;
- gateways de pagamento.

Artigos públicos relevantes:

- `Liberação de Clientes`
- `Como gerar um Boleto?`
- `Como Funciona a Cobrança Automática?`
- `3 formas de aplicar desconto no boleto do cliente`
- `Emitindo relatórios financeiros`
- `Integrando Gateway Efí/Asaas/Cel_cash/Cora/Wide Pay/Iugu/Lytex`

Regra para Hermes:

- consultas financeiras podem ser read-only;
- liberação, desconto, baixa, edição de boleto, exclusão ou alteração de vencimento exigem aprovação humana e política do provedor.

### Liberação de cliente

O helpdesk descreve liberação por fatura em atraso:

```text
Financeiro -> localizar fatura em atraso -> Editar -> Situação: Observação -> Data da Observação -> Atualizar
```

A data de observação define até quando o cliente fica liberado por confiança/aguardando compensação.

Cuidados:

- confirmar titularidade e política de liberação;
- checar se há outras faturas em atraso;
- registrar motivo e atendente;
- não liberar automaticamente por pedido do cliente final sem regra explícita.

### Chamados / Ordens de serviço

Caminho:

```text
Chamados > Todos > Novo Chamado
```

Campos públicos citados:

- Cliente: obrigatório;
- Categoria: Instalação, Suporte, Financeiro, Outros;
- Responsável;
- Prioridade: baixa, média, alta;
- Assunto: obrigatório;
- Mensagem: obrigatória.

Ao criar chamado a documentação cita envio de e-mail para cliente, responsável e usuário que registrou.

Modelo de chamado gerado pelo Hermes:

```text
Cliente/contrato: <mascarado>
Categoria: Suporte / Financeiro / Instalação / Outros
Prioridade: baixa/média/alta
Assunto: <resumo curto>
Mensagem:
- Relato: <queixa do cliente>
- Diagnóstico: <financeiro/PPPoE/OLT/Zabbix/DNS/etc.>
- Evidências: <sem segredos>
- Próximo passo sugerido: <ação técnica>
```

### Logs / Auditoria

O helpdesk cita:

- `Logs > Conexões`
- `Cadastro do Cliente > Logs de Conexão`
- `Monitoramento > Clientes On/Off`
- em problema de logs: validar se a RB registra eventos em `LOGS` e `PPP Actives`.

Uso com Hermes:

- consultar logs antes de concluir queda/intermitência;
- comparar log Beesweb com log da RB/Radius;
- se RB registra e Beesweb não, revisar integração do servidor e acionar suporte Beesweb.

## Fluxo para atendimento WhatsApp/Hermes

### Pré-atendimento financeiro

```text
Cliente relata boleto/bloqueio
  -> identificar cliente/contrato
  -> consultar financeiro no Beesweb
  -> se pendência: orientar canal oficial / enviar segunda via se integração permitir
  -> se comprovante/liberação: abrir chamado financeiro ou pedir aprovação interna
```

### Pré-atendimento técnico

```text
Cliente relata sem conexão/lentidão
  -> identificar cliente/contrato/login
  -> consultar autenticação no Beesweb
  -> consultar logs/conexões
  -> consultar servidor/cliente online quando disponível
  -> consultar OLT/ONU ou CTO quando aplicável
  -> abrir chamado Beesweb com diagnóstico anexado se não resolver
```

### Dashboard NOC

Integra bem com a skill `dashboard-noc-diagnostico-cliente`:

```text
Login PPPoE -> sessão/logs -> AP/OLT/CTO -> DNS/HTTP -> relatório -> chamado Beesweb
```

## Possível integração via API

Como não foi encontrada API pública oficial, use este padrão quando o fornecedor ou o provedor fornecer documentação:

Variáveis em `.env`:

```bash
BEESWEB_BASE_URL="https://app.beesweb.com.br"
BEESWEB_API_URL="https://api-ou-endpoint-fornecido"
BEESWEB_TOKEN="token-no-cofre"
BEESWEB_READ_ONLY="true"
BEESWEB_TIMEOUT="20"
```

Ferramentas recomendadas:

```text
beesweb_cliente_lookup(telefone|cpf|contrato|login)
beesweb_contrato_status(cliente_id|contrato_id)
beesweb_financeiro_status(cliente_id|contrato_id)
beesweb_autenticacao_lookup(login)
beesweb_chamado_open(cliente_id, categoria, prioridade, assunto, mensagem)
beesweb_chamado_append(chamado_id, mensagem)
beesweb_cto_lookup(login|cto_id)
beesweb_server_status(server_id)
```

Separar ferramentas de leitura e escrita. Em produção, deixar `BEESWEB_READ_ONLY=true` até validar fluxo com dados fake.

## Browser automation quando não houver API

Use browser automation apenas em contexto controlado:

1. operador logado manualmente;
2. Hermes navega somente onde foi solicitado;
3. não digitar senhas nem tokens;
4. capturar evidência mínima;
5. pedir confirmação antes de clicar em salvar/atualizar/liberar/excluir.

Ações que exigem confirmação:

```text
Salvar cliente/contrato/autenticação
Liberar cliente por observação
Gerar/editar/excluir boleto
Criar/fechar chamado
Executar importação/exportação com RB
Criar/conectar servidor
Cadastrar OLT e autorizar ONU
Edição em lote
```

## Respostas padrão

### Cliente com suspeita financeira

```text
Identifiquei que a situação pode estar relacionada ao financeiro. Vou encaminhar para a fila financeira com o contrato e a pendência resumida, sem expor dados sensíveis.
```

### Cliente técnico com diagnóstico

```text
Fiz a triagem inicial: contrato identificado, autenticação verificada e logs consultados. Vou abrir/atualizar o chamado com essas informações para o suporte técnico não começar do zero.
```

### Operador NOC

```text
Antes de alterar algo no Beesweb, vou consultar cliente, contrato, autenticação e logs. Se precisar ação de escrita, eu te mostro o impacto e peço confirmação.
```

## Armadilhas comuns

1. **Reutilizar script de servidor**: cada servidor Beesweb tem script próprio; reutilizar pode gerar erro de comando.
2. **Abrir API MikroTik 8728 sem controle**: preferir VPN/ACL; se exposto, limitar origem e credencial.
3. **Telnet de OLT exposto**: usar VPN/ACL/port forwarding controlado; evitar porta 23 aberta na internet.
4. **Liberar cliente automaticamente**: liberação por observação deve seguir política financeira e auditoria.
5. **Importação/exportação em massa sem backup**: pode afetar secrets, profiles, pools e autenticações.
6. **Misturar atendimento cliente com comando admin**: cliente final não aprova ações; aprovação vem de operador interno.
7. **Expor dados no WhatsApp/grupo**: mascarar CPF/CNPJ, telefone, endereço, login e valores.

## Checklist de validação

- [ ] Cliente/contrato identificado com segurança mínima.
- [ ] Dados sensíveis mascarados.
- [ ] Consulta read-only feita antes de escrita.
- [ ] Financeiro, contrato e autenticação verificados quando aplicável.
- [ ] Logs de conexão comparados com RB/Radius quando necessário.
- [ ] Chamado criado/atualizado com categoria, prioridade, assunto e mensagem.
- [ ] Ação de escrita teve aprovação humana.
- [ ] Evidência registrada sem senha/token/cookie.
