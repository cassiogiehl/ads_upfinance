# Quickstart: 001-movimentacoes

Prerequisites: 000-foundation is running and you are signed in as Rafael (see `../000-foundation/quickstart.md`).

## Scenario (UI)

1. Open **Movimentações** with no data. You see the empty state "Você ainda não tem movimentações" with a register button (UC03 FA01).
2. **Nova movimentação** → ENTRADA, "Salário outubro", `5.000,00`, category Salário → Save. It appears at the top of the list (US1-1).
3. Register a SAIDA, "Aluguel", `1.500,00`, Moradia. The list shows the badge **Essencial** (US1-2, RN002).
4. Try to save with an empty description. The field error asks for the missing data (FA01).
5. Try the amount `0` and then `-10`. The amount error appears (FA02).
6. With the type set to SAIDA, open the category select. Only spending categories appear, each with its pilar (US2-1).
7. In the list, change "Aluguel" to the category Lazer. The badge changes to **Pessoal** (UC02).
8. Filter the list by type SAIDA and by the current month (US3-4).

## Scenario (API)

```bash
H="Authorization: Bearer $TOKEN"
curl -s -X POST localhost:8000/api/v1/movimentacoes -H "$H" -H 'Content-Type: application/json' \
  -d '{"descricao":"Aluguel","valor":"1500.00","tipo":"SAIDA","categoria_id":1}' | jq
curl -s -X POST localhost:8000/api/v1/movimentacoes -H "$H" -H 'Content-Type: application/json' \
  -d '{"descricao":"x","valor":"0","tipo":"SAIDA","categoria_id":1}' | jq .code     # "VALOR_INVALIDO"
curl -s "localhost:8000/api/v1/movimentacoes?tipo=SAIDA" -H "$H" | jq '.total'
```

## Automated

```bash
docker compose run --rm --no-deps api pytest tests -k movimentac -q
```
