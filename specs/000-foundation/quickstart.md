# Quickstart: 000-foundation

Validates the feature end to end on a fresh checkout.

## Run

```bash
docker compose up --build -d
docker compose exec api alembic upgrade head
# API docs: http://localhost:8000/docs   SPA: http://localhost:5173
```

## Scenario

1. Open the SPA, go to **Criar conta**, and register `Rafael` / `rafael@example.com` / `senha1234`. You land on the home screen (US1-1).
2. Sign out, then register the same email again. You see "Este e-mail já está cadastrado" (US1-2).
3. Sign in with a wrong password. You see a generic error (US2-2). Sign in correctly and you reach home (US2-1).
4. Sign out and open `/movimentacoes` directly. You are redirected to sign-in (US2-4).
5. API check:
   ```bash
   TOKEN=$(curl -s -X POST localhost:8000/api/v1/auth/login \
     -H 'Content-Type: application/json' \
     -d '{"email":"rafael@example.com","senha":"senha1234"}' | jq -r .access_token)
   curl -s localhost:8000/api/v1/categorias -H "Authorization: Bearer $TOKEN" | jq
   curl -s localhost:8000/api/v1/pilares -H "Authorization: Bearer $TOKEN" | jq
   ```
   Every SAIDA category has a pilar, every ENTRADA category has `pilar: null`, and the pilares read 0.50 / 0.30 / 0.20 (US3).
6. Resize the browser to 360 px. There is no horizontal scrolling on login, register or home (US4).

## Automated

```bash
cd backend && pytest -q
cd frontend && npm test
```
