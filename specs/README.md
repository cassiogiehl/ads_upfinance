# UPFinance: Specifications (Spec-Driven Development)

These specs turn the Sprint 2–4 analysis into buildable features, following the [GitHub Spec Kit](https://github.com/github/spec-kit) layout. The governing principles are in [`.specify/memory/constitution.md`](../.specify/memory/constitution.md).

## How to use

1. Pick the next feature in order (000 → 004).
2. Read `spec.md` (what and why), then `plan.md` (how), `research.md`, `data-model.md` and `contracts/openapi.yaml`.
3. Resolve or accept its `[NEEDS CLARIFICATION]` items (see below).
4. Implement `tasks.md` top to bottom. Tests are written first and must fail before the implementation tasks.
5. Validate with `quickstart.md`, then move to the next feature.

Every file per feature:

| File | Purpose |
|---|---|
| `spec.md` | User stories, acceptance scenarios, FRs, success criteria. **Tech-agnostic** |
| `research.md` | Decisions with rationale and alternatives. Provisional defaults for open questions |
| `data-model.md` | Entities, fields, constraints, mapping from the Sprint 4 class diagram (Δ = refinement) |
| `contracts/openapi.yaml` | REST endpoints for the feature (OpenAPI 3.1) |
| `plan.md` | Architecture, files, Constitution Check |
| `quickstart.md` | Manual end-to-end validation scenario |
| `tasks.md` | Ordered, numbered tasks. `[P]` = parallelizable |

## Features

| # | Feature | Sprint user stories | RF | UC | AD | Priority |
|---|---|---|---|---|---|---|
| [000](000-foundation/spec.md) | Foundation: account, auth, category catalog, skeleton | — | RF003 | — | — | Prerequisite |
| [001](001-movimentacoes/spec.md) | Register, categorize and view movements | US01, US02, US03 | RF001–RF004 | UC01–UC03 | AD01 | High |
| [002](002-analise-50-30-20/spec.md) | 50-30-20 analysis and limit alerts | US04, US05 | RF005–RF007 | UC04–UC06 | AD02 | High |
| [003](003-fatura-pdf/spec.md) | Credit-card invoice upload and interpretation | US06, US07 | RF008, RF009 | UC07, UC08 | AD03 | Medium |
| [004](004-recorrencias/spec.md) | Recurring payments and alerts | US08, US09 | RF010, RF011 | UC09, UC10 | AD04 | Medium |

## Traceability matrix

| RF | UC | Spec | Business rules | Classes (Sprint 4) |
|---|---|---|---|---|
| RF001 | UC01 | 001 US1 | — | Usuario, Movimentacao, TipoMovimentacao |
| RF002 | UC02 | 001 US2 | RN002 | Movimentacao, Categoria |
| RF003 | UC02 | 000 US3, 001 US2 | RN002 | Categoria, Pilar |
| RF004 | UC03 | 001 US3 | — | Usuario, Movimentacao |
| RF005 | UC04 | 002 US1 | RN001, RN003, RN004 | AnaliseFinanceira, DistribuicaoPilar, Pilar |
| RF006 | UC05 | 002 US2 | RN001, RN003, RN004 | AnaliseFinanceira |
| RF007 | UC06 | 002 US3, US4 | RN003 | Alerta, AlertaLimite |
| RF008 | UC07 | 003 US1 | — | Fatura, StatusFatura |
| RF009 | UC08 | 003 US2, US3 | — | InterpretadorFatura, InterpretadorFaturaPDF, Movimentacao |
| RF010 | UC09 | 004 US1, US4 | — | IdentificadorRecorrencia, PagamentoRecorrente |
| RF011 | UC10 | 004 US2, US3 | — | Alerta, AlertaRecorrencia |
| RNF001, RNF002 | — | 000 US4 (all features) | — | — |

## Changes to the Sprint 4 class diagram (Δ)

| Change | Where | Why |
|---|---|---|
| `Categoria.tipo` added; `pilar` is null for income categories | 000 research R2 | Income does not belong to a spending pilar, but RF001 requires every movement to have a category |
| `ItemFatura` (draft) added | 003 data-model | AD03 requires user review before movements are created |
| `StatusFatura.CONFIRMADA` added | 003 research R7 | Prevents importing the same invoice twice |
| `InterpretadorFatura.interpretar()` returns draft items instead of `Movimentacao` | 003 data-model | Movements are created only after confirmation |
| `PagamentoRecorrente`: `descricao_normalizada`, `frequencia`, `ultima_ocorrencia`, `descartado` added | 004 data-model | Grouping key, projection, inactivity, dismissal |
| `AlertaRecorrencia.motivo` added | 004 research R4 | Distinguishes "identified" from "due soon" alerts |
| `AlertaLimite` has the period (`periodo_inicio`/`fim`) | 002 research R2 | One alert per pilar per period (multiplicity 0..3) |
| Auth (`Usuario.senha_hash`, JWT) | 000 research R1 | `Usuario` owns all data, and the app is Web-accessible |

## Open questions (`[NEEDS CLARIFICATION]`)

Each one has a provisional default in the feature's `research.md`, so the work is not blocked.

| # | Feature | Question | Provisional default |
|---|---|---|---|
| 1 | 001 | Must the user always enter the movement date? | Optional, defaults to today |
| 2 | 001 | Can movements be edited or deleted? | No, only recategorized (UC02) |
| 3 | 002 | Is the analysis period always a calendar month? | Current month by default, any range allowed |
| 4 | 002 | Should alerts also fire when an expense is registered (not only on analysis)? | Yes, for the current month |
| 5 | 002 | Is Futuro a ceiling (RN003 literal) or a savings target? | Ceiling, per RN003 |
| 6 | 003 | Which banks' invoice layouts must v1 support? | One generic line-pattern interpreter |
| 7 | 004 | Interval and amount tolerances for recurrence | Monthly 25–35 days; amounts within ±30% of the median |
| 8 | 004 | Reminder window before the due date | 3 days |
| 9 | 004 | Can the user dismiss a false-positive recurrence? | Yes |

## Target repository layout (after implementation)

```
.specify/memory/constitution.md
specs/                     # this folder
backend/                   # FastAPI (see 000-foundation/plan.md)
frontend/                  # React + Vite + TS
docker-compose.yml
Sprint 2 - … .md, Sprint 3 - … .md, Sprint4_… .md   # original analysis (read-only)
```
