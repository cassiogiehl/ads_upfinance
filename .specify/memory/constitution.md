# UPFinance Constitution

These principles govern every specification, plan and task in `specs/`. Each feature's `plan.md` contains a **Constitution Check** that must pass before implementation starts. Any violation must be justified in that plan's *Complexity Tracking* table.

Sources of truth for product behavior (read-only):
- `Sprint 2 - Elicitação de Requisitos.md`: RF001–RF011, RNF001–RNF002, RN001–RN004, US01–US09, acceptance criteria, backlog
- `Sprint 3 - Diagrama UML (Refinamento).md`: UC01–UC10 and their alternative flows (FA)
- `Sprint4_Wiki_AzureDevOps.md`: activity diagrams AD01–AD04, class diagram, modeling decisions

---

## I. Traceability

Every functional requirement in a `spec.md` and every task in a `tasks.md` cites the sprint IDs it implements (RFxxx, UCxx, RNxxx, USxx, ADxx).

A spec must not add behavior that has no source in Sprints 2–4. A gap is either:
- marked `[NEEDS CLARIFICATION: …]` in `spec.md`, or
- resolved as an explicit decision in `research.md`, with its rationale.

## II. Fixed v1 scope

Out of scope for v1, and must not be specified or built:
- automatic integration with banks or cards
- payments or transfers
- any LLM or AI service

The 50-30-20 distribution is fixed and cannot be configured (RN004). The financial interpretation is deterministic and rule-based (RF006).

## III. Test-first (non-negotiable)

- Contract tests and integration tests are written, and seen to fail, before the implementation tasks that satisfy them.
- Every acceptance criterion in Sprint 2 §10 maps to at least one automated test.
- Every alternative flow (FA) in Sprint 3 maps to at least one test.

## IV. Money correctness

- Monetary amounts use exact decimal arithmetic (`Decimal` / `NUMERIC(12,2)`). Floating point is never used for money.
- `valor` is always strictly positive. The direction comes from `tipo` (ENTRADA / SAIDA).
- Percentages and limits are computed with `Decimal` and rounded half-up to 2 decimal places only for presentation.

## V. Data ownership

- Every persisted record belongs to exactly one `Usuario`, following the compositions in the class diagram.
- Every query is scoped to the authenticated user.
- Accessing another user's resource returns 404, not 403, so its existence is not leaked.

## VI. Simplicity

- One backend service, one database, one SPA frontend.
- No repository or interface abstraction unless a real variation exists.
- The one justified exception is `InterpretadorFatura` (a strategy per invoice layout), because invoice formats vary (Sprint 2 risk, Sprint 4 §3.4).
- Derived data is computed rather than stored. `AnaliseFinanceira` and `DistribuicaoPilar` are computed on request.

## VII. Technology baseline

| Concern | Choice |
|---|---|
| Backend | Python 3.12, FastAPI, Pydantic v2 |
| Persistence | SQLAlchemy 2.x (typed ORM), Alembic migrations, PostgreSQL 16 (SQLite in-memory for tests) |
| Auth | Email + password (argon2 hash), JWT bearer access token |
| PDF | `pdfplumber` (see `specs/003-fatura-pdf/research.md`) |
| Backend tests | pytest, httpx `TestClient`, coverage ≥ 80% on `services/` |
| Frontend | React 18 + TypeScript + Vite, React Router, TanStack Query |
| Frontend tests | Vitest + Testing Library |
| UI | Responsive, mobile-first, works on phone and desktop browsers (RNF001, RNF002) |
| Runtime | Docker Compose: `db`, `api`, `web` |
| CI | Lint (ruff, eslint), type-check (mypy, tsc), tests on every push |

## VIII. Conventions

- **Language:** code identifiers and docs are in English, except domain terms, which keep the Portuguese names from the class diagram (`Movimentacao`, `Categoria`, `Pilar`, `Fatura`, `PagamentoRecorrente`, `Alerta`…). Text shown to users is in Brazilian Portuguese.
- **API:** REST + JSON with snake_case fields. Errors use the shape `{"code": "UPPER_SNAKE", "message": "...", "details": {...}}`. Each FA has a stable `code`.
- **Layers:** `api/` (routers, HTTP only) → `services/` (use-case logic and business rules) → `models/` (ORM). Business rules live only in `services/`.

## Governance

- This constitution takes precedence over feature plans. Changing it requires updating the version below and re-running the Constitution Check of every open plan.
- Version: 1.0.0. Ratified: 2026-10-25.
