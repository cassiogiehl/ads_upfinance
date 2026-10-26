# Quickstart: 002-analise-50-30-20

Prerequisites: 001 is running and you are signed in as a fresh user.

## Seed the worked example (spec US1-1)

Register these movements, all dated in the current month:

| Tipo | Descrição | Valor | Categoria (pilar) |
|---|---|---|---|
| ENTRADA | Salário | 10.000,00 | Salário |
| SAIDA | Aluguel | 2.500,00 | Moradia (Essencial) |
| SAIDA | Mercado | 1.500,00 | Alimentação (Essencial) |
| SAIDA | Viagem | 3.500,00 | Viagens (Pessoal) |
| SAIDA | Aporte | 1.000,00 | Investimentos (Futuro) |

## Scenario

1. Before seeding, open **Análise**. You see the message that records are needed (UC04 FA01).
2. After seeding, open **Análise** for the current month. You should see:
   - Essencial 4.000,00 / 5.000,00 (80%), within the limit
   - Pessoal 3.500,00 / 3.000,00 (116,67%), **exceeded by R$ 500,00**
   - Futuro 1.000,00 / 2.000,00 (50%), within the limit
   - Summary: renda 10.000,00, gastos 8.500,00, saldo 1.500,00
3. The interpretation contains the Pessoal-exceeded sentence and the "Atenção: 1 pilar(es)…" conclusion (UC05 FA02).
4. The bell shows **1**. **Alertas** lists one Pessoal alert. Mark it as read and the bell clears (UC06).
5. Reload **Análise** several times. There is still only one alert (research R2).
6. Proactive trigger (US4): register a Pessoal expense of 100,00. The Pessoal alert is updated (excedente 600,00) and becomes unread again.
7. Analyze the previous month (empty). You see the insufficient-data message and no new alert.

## API

```bash
curl -s "localhost:8000/api/v1/analise" -H "Authorization: Bearer $TOKEN" | jq '.distribuicoes, .interpretacao'
curl -s "localhost:8000/api/v1/alertas?lido=false" -H "Authorization: Bearer $TOKEN" | jq '.total_nao_lidos'
```
