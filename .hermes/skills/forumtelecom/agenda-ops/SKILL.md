---
name: agenda-ops
description: "Use when the user asks Hermes to manage agenda, calendar, reminders, appointments, follow-ups, meeting schedules, service windows, recurring tasks, technician visits, or operational planning. Guides safe use of Google Calendar/Workspace, Hermes cron reminders, WhatsApp confirmations, and structured scheduling without exposing personal data."
version: 1.0.0
author: Hermes Tutor
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [agenda, calendar, reminders, cron, google-calendar, whatsapp, operations]
    related_skills: [google-workspace, teams-meeting-pipeline]
---

# Agenda Operations

Use esta skill para atuar como assistente de agenda operacional: compromissos, reuniões, janelas de manutenção, retornos comerciais, visitas técnicas e lembretes via Hermes.

## Postura operacional

1. **Confirmar intenção antes de criar evento externo**: criar/alterar/cancelar evento em Google Calendar, agenda corporativa ou enviar convite tem efeito externo. Se o pedido estiver claro, execute; se faltar data/horário/fuso/destinatários, peça somente o dado faltante.
2. **Privacidade**: não expor telefones, e-mails, links de reunião privados, endereços completos ou observações sensíveis no grupo.
3. **Fuso horário**: assumir `America/Sao_Paulo` quando o usuário estiver no Brasil e não informar outro fuso. Para cálculo de datas/horas, use ferramenta (`date`, Python ou API), não chute.
4. **Resumo curto**: ao finalizar, responder com data, horário, título e próximo passo.

## Quando usar

- marcar reunião ou visita;
- criar lembrete único ou recorrente;
- consultar agenda do dia/semana;
- reagendar/cancelar compromisso;
- criar janela de manutenção com checklist;
- acompanhar pendências com retorno programado.

## Entrada mínima para agendar

Coletar ou inferir:

- título objetivo;
- data;
- horário de início;
- duração ou horário de fim;
- fuso horário;
- participantes, se houver convite;
- canal/local: WhatsApp, Google Meet, presencial, remoto, NOC etc.;
- recorrência, se houver.

Se só faltar um campo, pergunte curto:

```text
Qual horário e duração?
```

## Comandos e caminhos úteis

### Lembrete pelo Hermes cron

Para lembretes dentro do Hermes/WhatsApp, usar cronjob com prompt autossuficiente:

```text
schedule: 2026-07-08T15:00:00-03:00
prompt: "Lembrar Fernando: revisar chamados pendentes do NOC. Responder em português, curto."
deliver: origin
attach_to_session: true
```

Para recorrente:

```text
schedule: "0 9 * * 1-5"
prompt: "Enviar lembrete diário: revisar agenda e pendências operacionais do dia."
```

### Google Calendar / Workspace

Quando existir integração Google Workspace (`gws`), preferir criar eventos reais pelo calendário. Antes de escrever:

```bash
gws calendar list
```

Operação segura:

1. consultar calendários disponíveis;
2. escolher calendário correto;
3. criar/alterar evento;
4. ler de volta o evento criado e reportar ID/link sem expor dados privados.

## Janelas de manutenção

Modelo mínimo:

```text
Título: Janela de manutenção - <ambiente>
Início: <data hora>
Fim: <data hora>
Impacto: <sem impacto / risco / indisponibilidade prevista>
Plano: <3 passos>
Rollback: <como voltar>
Contato: <responsável, sem expor telefone no grupo>
```

## Armadilhas comuns

1. **Agendar sem fuso**: sempre resolver fuso antes de criar.
2. **Confundir lembrete com evento**: lembrete simples pode ser cronjob; reunião com participantes deve ir para Calendar.
3. **Expor link privado**: em grupo, resumir; se precisar, enviar em canal seguro.
4. **Evento recorrente sem fim**: confirmar periodicidade e, quando possível, data de término.
5. **Prometer agenda sem verificar**: após criar, consultar o evento de volta.

## Checklist de validação

- [ ] data/hora/fuso confirmados;
- [ ] duração definida;
- [ ] canal/local definido;
- [ ] participantes tratados com privacidade;
- [ ] evento/lembrete criado na ferramenta correta;
- [ ] criação validada por leitura de volta;
- [ ] resposta final curta com próximo passo.
