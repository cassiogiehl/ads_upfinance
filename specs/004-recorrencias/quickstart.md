# Quickstart: 004-recorrencias

Prerequisites: 001 and 002 are running and you are signed in as a fresh user.

## Seed

Register these SAIDA movements. Use dates relative to today (D = today):

| Descrição | Valor | Data | Categoria |
|---|---|---|---|
| Conta de luz 07/2026 | 180,00 | D − 89 | Contas da casa |
| Conta de luz 08/2026 | 195,00 | D − 59 | Contas da casa |
| CONTA LUZ 09/2026 | 172,00 | D − 29 | Contas da casa |
| Internet Vivo | 119,90 | D − 58 | Contas da casa |
| Internet Vivo | 119,90 | D − 28 | Contas da casa |
| iFood | 45,00 | D − 20 | Restaurantes e delivery |
| iFood | 82,00 | D − 3 | Restaurantes e delivery |
| Geladeira | 3.200,00 | D − 40 | Compras |

## Scenario

1. After the last movement is saved, open **Recorrências**. You see:
   - "Conta de luz": Mensal, about R$ 182,33, next due date about D + 1…2, 3 occurrences. The three description variants are grouped together (US1-5).
   - "Internet Vivo": Mensal, R$ 119,90, next due date about D + 2.
   - **No** iFood (17-day interval fits no frequency band) and **no** Geladeira (one occurrence) (UC09 FA01).
2. **Alertas** shows 2 "Identificamos um pagamento recorrente…" alerts (UC10), plus "vence em N dia(s)" reminders for the recurrences due within 3 days (US3).
3. Click **Analisar histórico agora** again. No new alerts appear (US2-4, SC-003).
4. Register "Internet Vivo" 119,90 dated today. The next due date of Internet Vivo moves forward about a month, and no reminder appears for the paid cycle (US3-2).
5. Expand "Conta de luz". Its 3 source movements are listed (US4-2).
6. Choose **Não é recorrente** on one recurrence. It moves to Descartados and its unread alerts are cleared (US5).

## API

```bash
curl -s -X POST localhost:8000/api/v1/recorrencias/identificar -H "Authorization: Bearer $TOKEN" | jq '.novas, .itens[].descricao'
curl -s "localhost:8000/api/v1/alertas?tipo=RECORRENCIA" -H "Authorization: Bearer $TOKEN" | jq '.items[].mensagem'
```
