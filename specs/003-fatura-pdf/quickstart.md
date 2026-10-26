# Quickstart: 003-fatura-pdf

Prerequisites: 001 (and ideally 002) is running and you are signed in.

## Generate sample invoices

```bash
# ./backend is bind-mounted at /app, so the files appear on the host in backend/.faturas/ (git-ignored)
docker compose run --rm --no-deps api python -m tests.fixtures.gerar_faturas --out /app/.faturas
# creates: generica.pdf, virada_ano.pdf, com_pagamentos.pdf, vazia.pdf, imagem.pdf, protegida.pdf
```

## Scenario

1. **Faturas → Enviar**: select `backend/.faturas/generica.pdf`. The review screen lists every purchase line with date, description, amount and a suggested category (UBER → Transporte, IFOOD → Restaurantes e delivery, NETFLIX → Assinaturas).
2. Try uploading a `.jpg` renamed to `.pdf`. You see "Envie a fatura em formato PDF", and you can pick another file right away (UC07 FA01).
3. Upload `vazia.pdf`, then `imagem.pdf`. Both show "A fatura não pôde ser interpretada" (UC08 FA01), and no movements are created.
4. Upload `com_pagamentos.pdf`. Lines like "PAGAMENTO RECEBIDO" and the refunds are absent from the review list (research R5).
5. Upload `virada_ano.pdf` (due in January). December purchases are dated in the previous year (research R4).
6. On the review screen, untick one item, clear the category of another, and try to confirm. The button stays disabled, or the server highlights the row. Choose a category and confirm. You are redirected to **Movimentações**, where the items appear as SAIDA.
7. Upload `generica.pdf` again. You see "Esta fatura já foi enviada" (409).
8. **Análise** now includes the imported expenses. The limit alerts are updated if a pilar crossed its limit.
9. **Faturas**: the history shows each upload with its status and counts.

## API

```bash
curl -s -X POST localhost:8000/api/v1/faturas -H "Authorization: Bearer $TOKEN" \
  -F arquivo=@backend/.faturas/generica.pdf | jq '.status, (.itens | length)'
```
