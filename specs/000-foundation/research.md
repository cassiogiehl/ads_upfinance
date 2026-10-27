# Research: 000-foundation

## R1: Authentication mechanism

- **Decision:** email and password, with passwords hashed using argon2 (`argon2-cffi` via `pwdlib`). The API issues a stateless JWT access token (HS256, valid for 8 hours). The SPA stores it in memory and in `sessionStorage`. There is no refresh token in v1.
- **Rationale:** the sprints define a single actor who owns data (`Usuario` compositions), so some form of identity is needed. This is the simplest secure option for one SPA plus one API, and it adds no external identity provider, keeping the v1 scope.
- **Alternatives considered:** server-side sessions with cookies (they need CSRF handling across SPA and API origins); OAuth or social login (an external dependency with no source in the sprints); no auth at all, single user (contradicts the Web-accessible, multi-user nature implied by `Usuario` having an `id` and an `email`).

## R2: Category catalog content

- **Decision:** seed the following catalog through a migration. It is read-only for users.

| Pilar | Categorias |
|---|---|
| ESSENCIAL | Moradia, Contas da casa (água, luz, gás, internet), Alimentação (mercado), Transporte, Saúde, Educação |
| PESSOAL | Lazer, Restaurantes e delivery, Compras, Assinaturas, Viagens, Cuidados pessoais |
| FUTURO | Investimentos, Reserva de emergência, Previdência, Pagamento de dívidas |
| (ENTRADA only) | Salário, Renda extra, Outras entradas |

- **Rationale:** RN002 requires categories to come pre-associated with a pilar. The sprints don't list them, so this list follows common 50-30-20 guidance and the glossary examples (água, luz, internet).
- **Income categories:** the class diagram gives `Categoria` a mandatory `pilar`, but income does not belong to a spending pilar. **Decision:** `Categoria.pilar` is nullable, and a new field `Categoria.tipo` (ENTRADA | SAIDA) is added. SAIDA categories MUST have a pilar (RN002). ENTRADA categories have none and only count toward renda. This is a refinement of the Sprint 4 class diagram and is noted in `data-model.md`.
- **Alternatives considered:** forcing income into a pilar (meaningless for the analysis); allowing ENTRADA movements to have no category (contradicts RF001, which says every movement has a category).

## R3: Project structure

- **Decision:** a monorepo with `backend/` (FastAPI) and `frontend/` (Vite React) at the root, plus `docker-compose.yml`. The existing sprint documents stay where they are.
- **Rationale:** one repository for a small team and a single deployable system (Constitution VI).

## R4: Database for tests

- **Decision:** PostgreSQL in Docker for development. SQLite in-memory for unit and integration tests. The schema must stay portable: `NUMERIC(12,2)`, ENUMs stored as `VARCHAR` with CHECK constraints instead of native PG enums.
- **Rationale:** fast tests that need no running `db` service (`docker compose run --rm --no-deps api pytest`, see R5). Using `VARCHAR` with CHECK keeps Alembic migrations identical on both databases.

## R5: Docker Compose as the only runtime

- **Decision:** the whole application runs in Docker Compose (Constitution IX). The host only needs Git, Docker Engine and Docker Compose v2.
  - `db`: `postgres:16`, named volume `pgdata`, healthcheck `pg_isready`, port 5432 published for local inspection only.
  - `api`: built from `backend/Dockerfile` (`python:3.12-slim`, runtime and dev dependencies so tests and lint run in the same image). Its entrypoint runs `alembic upgrade head` and then `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`. `depends_on: db: condition: service_healthy`. `./backend` is bind-mounted to `/app`. Port 8000.
  - `web`: built from `frontend/Dockerfile` (`node:22-alpine`, `npm ci`). Runs `vite --host 0.0.0.0 --port 5173`. `./frontend` is bind-mounted to `/app`, with an anonymous volume on `/app/node_modules` so the host never needs its own `node_modules`. The Vite dev server proxies `/api` to `http://api:8000`, so the SPA uses relative URLs. Port 5173.
  - Configuration: `.env.example` (committed) holds `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `DATABASE_URL`, `JWT_SECRET` and `JWT_TTL_HOURS` with development values. Compose reads `.env`, which is git-ignored.
  - Commands: `docker compose run --rm --no-deps api pytest`, `… api ruff check .`, `… api mypy app`, `docker compose run --rm --no-deps web npm test`, `… web npm run lint`, `… web npx tsc --noEmit`.
- **Rationale:** one command brings up the same environment on every machine and in CI, nobody fights local Python or Node versions, and the automatic migration on startup means a fresh clone works with `docker compose up --build`.
- **Alternatives considered:** running backend and frontend on the host with only the database in Docker (setup differs per machine and drifts from CI); a separate migration service (one more service against Constitution VI, for no gain at this size); serving a production build of the SPA from nginx in v1 (not needed for the course scope; it can be added later as a build stage of `frontend/Dockerfile` without changing the services).

