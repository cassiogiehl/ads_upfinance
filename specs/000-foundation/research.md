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
- **Rationale:** fast tests without Docker in CI. Using `VARCHAR` with CHECK keeps Alembic migrations identical on both databases.
