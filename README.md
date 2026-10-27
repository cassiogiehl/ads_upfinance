# UPFinance

Personal finance web app built around the 50-30-20 rule: register income and expenses, see how spending splits across the Essencial (50%), Pessoal (30%) and Futuro (20%) pilares, import credit-card invoices and track recurring payments.

The project follows Spec-Driven Development. Requirements come from the sprint analysis in [`elicitacoes/`](elicitacoes/), and every feature is specified in [`specs/`](specs/README.md) under the rules of the [constitution](.specify/memory/constitution.md).

## Prerequisites

Only **Git**, **Docker Engine** and **Docker Compose v2**. Python, Node.js and PostgreSQL are never installed on the host: everything runs in containers (Constitution IX).

## Run

```bash
cp .env.example .env
docker compose up --build -d
```

| Service | URL | What it is |
|---|---|---|
| `web` | http://localhost:5173 | React SPA (Vite dev server, proxies `/api` to `api`) |
| `api` | http://localhost:8000/docs | FastAPI, interactive API docs |
| `db` | `localhost:5432` | PostgreSQL 16 |

The `api` service applies the database migrations on startup, so a fresh clone works with these two commands. Source code is bind-mounted, and both `api` and `web` reload on save.

```bash
docker compose logs -f api     # follow the API logs
docker compose down            # stop (keeps the database)
docker compose down -v         # stop and delete the database volume
```

## Test and lint

Every command runs inside a container. `--no-deps` skips the database: backend tests use an in-memory SQLite built from the real migrations.

```bash
# backend
docker compose run --rm --no-deps api pytest
docker compose run --rm --no-deps api pytest --cov   # coverage on services/, minimum 80%
docker compose run --rm --no-deps api ruff check .
docker compose run --rm --no-deps api mypy app

# frontend
docker compose run --rm --no-deps web npm test
docker compose run --rm --no-deps web npm run lint
docker compose run --rm --no-deps web npm run typecheck
```

Database migrations, when a feature adds one:

```bash
docker compose run --rm api alembic revision -m "describe the change"
docker compose run --rm api alembic upgrade head
```

## Configuration

All settings come from environment variables, read from `.env` (git-ignored). [`.env.example`](.env.example) has development defaults.

| Variable | Purpose |
|---|---|
| `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` | Database credentials |
| `DATABASE_URL` | SQLAlchemy URL used by `api` |
| `JWT_SECRET` | Token signing key, at least 32 characters (`openssl rand -hex 32`) |
| `JWT_TTL_HOURS` | Session length, 8 hours by default |
| `DB_PORT` | Host port for PostgreSQL, if 5432 is taken |

## Repository layout

```
.specify/memory/constitution.md   principles every spec and plan must follow
specs/                            one folder per feature: spec, plan, research, data model, contract, tasks
elicitacoes/                      sprint 2–4 analysis (requirements, UML, activity diagrams)
backend/                          FastAPI · SQLAlchemy · Alembic   (app/, tests/, alembic/)
frontend/                         React · TypeScript · Vite        (src/)
docker-compose.yml                db, api, web
```

## Features

| # | Feature | Status |
|---|---|---|
| [000](specs/000-foundation/spec.md) | Foundation: account, sign-in, category catalog | Done |
| [001](specs/001-movimentacoes/spec.md) | Register, categorize and view movements | Planned |
| [002](specs/002-analise-50-30-20/spec.md) | 50-30-20 analysis and limit alerts | Planned |
| [003](specs/003-fatura-pdf/spec.md) | Credit-card invoice upload | Planned |
| [004](specs/004-recorrencias/spec.md) | Recurring payments and alerts | Planned |

To work on a feature, follow [specs/README.md](specs/README.md#how-to-use): read its spec and plan, then implement `tasks.md` in order, tests first.
