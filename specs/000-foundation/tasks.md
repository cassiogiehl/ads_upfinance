# Tasks: 000-foundation

**Input:** [plan.md](plan.md), [data-model.md](data-model.md), [contracts/openapi.yaml](contracts/openapi.yaml)
**Covers:** RF003 · RN001, RN002, RN004 · RNF001, RNF002
**Legend:** `[P]` means it can run in parallel (different files, no dependency). `[USn]` is the user story in `spec.md`.

## Phase 1: Setup

- [ ] T001 Create `backend/pyproject.toml` with the dependencies from plan.md, plus ruff, mypy and pytest config
- [ ] T002 [P] Create the `frontend/` Vite React TS app (`package.json`, `vite.config.ts`, `tsconfig.json`) with react-router, @tanstack/react-query, vitest and @testing-library/react
- [ ] T003 [P] Create `backend/Dockerfile` and `backend/entrypoint.sh` (`alembic upgrade head`, then uvicorn with `--reload`), and `frontend/Dockerfile` (`npm ci`, `vite --host 0.0.0.0`), per research R5. Add `.dockerignore` files
- [ ] T004 [P] Create the CI workflow. It runs only Docker Compose commands: `docker compose build`, then in `api` ruff, mypy, pytest, and in `web` `tsc --noEmit`, eslint, vitest, `vite build` (Constitution IX)
- [ ] T005 Create `backend/app/core/config.py` (pydantic-settings), `backend/app/db.py` (engine, SessionLocal, Base) and `backend/app/main.py` (app factory, `/api/v1` prefix, CORS)
- [ ] T006 Create `backend/app/core/errors.py` with `DomainError` and handlers that produce `{code, message, details}`, mapping `RequestValidationError` to 422 `DADOS_INVALIDOS`
- [ ] T007 Initialize Alembic (`backend/alembic.ini`, `backend/alembic/env.py`) using `Base.metadata`
- [ ] T008 Create `backend/tests/conftest.py` with fixtures for an SQLite in-memory engine, `db`, `client`, `auth_headers` (registers and logs in user A) and `other_user_headers` (user B)
- [ ] T009 Create `docker-compose.yml` (`db` with healthcheck and named volume, `api` with `depends_on: service_healthy`, `web` with the `/api` proxy and a `node_modules` volume), `.env.example`, and add `.env` and `backend/.faturas/` to `.gitignore`. Check that `docker compose up --build` on a clean clone serves `/docs` and the SPA, and that `docker compose run --rm --no-deps api pytest` runs

## Phase 2: Tests first (they must fail)

- [ ] T010 [P] [US1] Contract test `POST /auth/register` (201, 409 `EMAIL_JA_CADASTRADO`, 422) in `backend/tests/contract/test_auth_register.py`
- [ ] T011 [P] [US2] Contract test `POST /auth/login` (200, 401 `CREDENCIAIS_INVALIDAS`, generic message) and `GET /usuarios/me` (401 without a token) in `backend/tests/contract/test_auth_login.py`
- [ ] T012 [P] [US3] Contract test `GET /categorias` and `GET /pilares` in `backend/tests/contract/test_categorias.py`: SAIDA categories have a pilar, ENTRADA categories have null, every pilar has ≥ 1 category, `?tipo=` filters
- [ ] T013 [P] Unit test `Pilar.calcular_limite(Decimal("10000"))` returns `5000.00`, `3000.00` and `2000.00` (RN003 example) in `backend/tests/unit/test_pilar.py`

## Phase 3: Core implementation

- [ ] T014 [P] Create `backend/app/domain/enums.py` with `Pilar` (StrEnum, `percentual`, `label`, `calcular_limite`) and `TipoMovimentacao` (makes T013 pass)
- [ ] T015 [P] Create `backend/app/models/usuario.py` and `backend/app/models/categoria.py` per data-model.md, including the CHECK constraints
- [ ] T016 Create the Alembic migration `0001_usuario_categoria.py`: tables plus the category seed from research R2
- [ ] T017 Create `backend/app/core/security.py`: argon2 hash and verify, JWT encode and decode (HS256, TTL from settings)
- [ ] T018 Create `backend/app/services/auth_service.py`: `register` (normalize email, check uniqueness) and `authenticate`
- [ ] T019 Create `backend/app/deps.py`: `get_db` and `get_current_user` (401 `NAO_AUTENTICADO`)
- [ ] T020 [P] Create `backend/app/schemas/auth.py` and `backend/app/schemas/categoria.py`
- [ ] T021 Create routers `auth.py`, `usuarios.py`, `categorias.py` and `pilares.py` in `backend/app/api/routers/` and register them in `main.py` (makes T010–T012 pass)

## Phase 4: Frontend

- [ ] T022 Create `frontend/src/api/client.ts`: base URL, bearer token injection, parsing of the error shape into a typed `ApiError`
- [ ] T023 Create `frontend/src/auth/AuthContext.tsx` (token in memory plus sessionStorage, login, register, logout) and `RequireAuth.tsx` (redirect to `/login`, keep the return path)
- [ ] T024 [P] [US1] Create `frontend/src/pages/RegisterPage.tsx` with field-level errors and the duplicate-email message
- [ ] T025 [P] [US2] Create `frontend/src/pages/LoginPage.tsx` with the generic error message
- [ ] T026 [US4] Create `frontend/src/components/Layout.tsx`: a responsive shell with nav (Movimentações, Análise, Faturas, Recorrências, Alertas) that collapses into a bottom bar or hamburger below 640 px
- [ ] T027 [P] Component tests for LoginPage and RegisterPage in `frontend/src/pages/__tests__/`

## Phase 5: Polish

- [ ] T028 Write `README.md` at the repo root: Docker and Docker Compose as the only prerequisites, `cp .env.example .env`, `docker compose up --build`, the `docker compose run` commands for tests and lint, and a link to `specs/`
- [ ] T029 Run quickstart.md manually on a machine with only Docker installed, including the 360 px check (SC-004)
- [ ] T030 Confirm CI is green

## Dependencies

T001/T002/T003 → T005 → T006/T007 → T008 → T009 → T010–T013 → T014–T021 → T022 → T023 → T024–T027 → T028–T030
