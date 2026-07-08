---
name: financeiro-ops
description: "Use when the user asks Hermes to help with financeiro/administrative routines: contas a pagar/receber, cobranças, conciliação, fluxo de caixa, vencimentos, notas/boletos, planilhas financeiras, dashboards simples, lembretes de pagamento, and safe handling of financial data without exposing secrets or personal banking details."
version: 1.0.0
author: Hermes Tutor
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [financeiro, contas-a-pagar, contas-a-receber, cobranca, fluxo-de-caixa, sheets, reports]
    related_skills: [google-workspace, airtable, notion, ocr-and-documents]
---

# Financeiro Operations

Use esta skill para rotinas financeiras administrativas e operacionais: contas a pagar/receber, vencimentos, cobranças, conciliação, fluxo de caixa simples, leitura de boletos/notas e geração de relatórios.

> Não é consultoria contábil, fiscal ou jurídica. Para decisão fiscal/tributária, orientar validar com contador/financeiro responsável.

## Segurança obrigatória

1. **Não expor dados sensíveis**: não publicar no grupo CPF/CNPJ completo, dados bancários, PIX, códigos de barras, boletos, tokens, credenciais, extratos completos ou contratos.
2. **Mascarar identificadores**: quando precisar citar, usar final parcial: `***1234`, `NF ****89`, `cliente A`.
3. **Confirmar antes de enviar cobrança externa**: mensagem para cliente, e-mail, WhatsApp ou baixa/cancelamento tem efeito externo.
4. **Não executar pagamento**: Hermes pode organizar, lembrar, conferir e preparar; pagamento real exige ação humana no banco/ERP.
5. **Fonte de verdade**: planilha, ERP, banco ou sistema informado pelo usuário prevalece sobre memória/conversa.

## Quando usar

- listar vencimentos do dia/semana;
- montar controle de contas a pagar/receber;
- gerar lembrete de cobrança;
- resumir inadimplência por cliente/período;
- criar planilha de fluxo de caixa;
- conciliar CSV/OFX/extrato exportado pelo usuário;
- extrair dados de boleto/NF/PDF;
- montar dashboard simples no Sheets/Airtable/Notion.

## Modelo mínimo de dados

Para contas a receber:

```text
cliente | documento | vencimento | valor | status | forma de pagamento | observação
```

Para contas a pagar:

```text
fornecedor | categoria | vencimento | valor | status | conta/centro de custo | observação
```

Status recomendado:

```text
aberto | vencido | pago | parcial | cancelado | em negociação
```

## Fluxo de trabalho seguro

1. **Receber fonte**: arquivo, planilha, export do ERP ou dados informados.
2. **Normalizar**: datas em `YYYY-MM-DD`, valores em BRL decimal, status padronizado.
3. **Validar totais**: conferir contagem de linhas, soma por status e período.
4. **Classificar**: aberto/vencido/pago, por cliente, fornecedor ou categoria.
5. **Gerar saída**: resumo curto, CSV/Sheets/Airtable/Notion quando pedido.
6. **Agendar lembrete**: usar `agenda-ops`/cronjob para vencimentos importantes.

## Comandos úteis

### Conferir CSV financeiro localmente

```bash
python3 - <<'PY'
import pandas as pd
from pathlib import Path
p = Path('financeiro.csv')
df = pd.read_csv(p)
print(df.shape)
print(df.head())
print(df.groupby('status')['valor'].sum())
PY
```

### Criar relatório simples em CSV

```bash
python3 - <<'PY'
import pandas as pd
# carregar, limpar, salvar resumo
PY
```

### Extrair texto de boleto/NF em PDF

Usar skill `ocr-and-documents` quando o usuário enviar PDF/imagem. Nunca devolver código de barras/PIX completo no grupo.

## Mensagem de cobrança — rascunho seguro

Antes de enviar, produzir rascunho e pedir confirmação:

```text
Olá, <nome>. Identificamos uma pendência com vencimento em <data>, no valor de <valor>. Pode verificar, por favor? Se já foi pago, desconsidere e nos envie o comprovante pelo canal combinado.
```

Não incluir ameaça, juros ou protesto sem regra definida pelo financeiro.

## Relatórios rápidos

Formato recomendado:

```text
Status financeiro: <período>
Receber aberto: R$ <total> (<qtd>)
Vencido: R$ <total> (<qtd>)
Pagar próximos 7 dias: R$ <total> (<qtd>)
Atenção: <maior risco>
Próximo passo: <ação objetiva>
```

## Armadilhas comuns

1. **Misturar competência com vencimento**: perguntar qual visão o usuário quer.
2. **Duplicar lançamento**: usar chave `cliente/fornecedor + documento + vencimento + valor` para deduplicar.
3. **Somar texto como número**: normalizar `R$ 1.234,56` para decimal antes de cálculo.
4. **Prometer pagamento automático**: Hermes não deve pagar; apenas preparar e lembrar.
5. **Enviar cobrança sem revisão humana**: sempre confirmar destinatário e conteúdo.

## Checklist de validação

- [ ] fonte de dados identificada;
- [ ] dados sensíveis mascarados;
- [ ] datas e valores normalizados;
- [ ] totais conferidos;
- [ ] relatório/arquivo gerado e validado;
- [ ] ações externas confirmadas pelo usuário;
- [ ] lembretes criados quando solicitado.
