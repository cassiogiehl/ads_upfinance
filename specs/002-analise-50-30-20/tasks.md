# Tasks: 002-analise-50-30-20

**Input:** [plan.md](plan.md), [data-model.md](data-model.md), [contracts/openapi.yaml](contracts/openapi.yaml)
**Prerequisite:** 001-movimentacoes is complete.
**Covers:** RF005, RF006, RF007 · UC04, UC05, UC06 · AD02 · RN001, RN003, RN004
**Legend:** `[P]` means it can run in parallel. US1/US2 = Sprint US04, US3/US4 = Sprint US05.

## Phase 1: Setup

- [ ] T200 Create `backend/app/models/alerta.py` (`Alerta` base with polymorphic `tipo`, `AlertaLimite`) and the migration `0003_alerta.py` with its CHECK, partial unique index and listing index (data-model.md)

## Phase 2: Tests first (they must fail)

- [ ] T201 [P] [US1] Unit test `domain.analise.calcular` in `backend/tests/unit/test_analise_calculo.py`: the worked example from spec US1-1 (exact Decimals), total == limit is not exceeded (RN003), renda > 0 with no expenses, expenses > renda gives a negative saldo, and limits always use 0.50/0.30/0.20 (RN001, RN004)
- [ ] T202 [P] [US2] (UC05 FA01/FA02) Unit test `domain.interpretacao.interpretar` in `backend/tests/unit/test_interpretacao.py`: the all-within text, the one-exceeded text (snapshot), the negative-saldo sentence, deterministic output (same input gives identical output), pt-BR currency and percentage format
- [ ] T203 [P] [US1] Unit test the insufficient-data guard: no movements, and renda = 0 with expenses, both return `DadosInsuficientes` (UC04 FA01)
- [ ] T204 [P] [US1] Contract test `GET /analise` in `backend/tests/contract/test_analise.py`: the `COMPLETA` shape has 3 distributions; `DADOS_INSUFICIENTES`; the default period is the current month; 422 `PERIODO_INVALIDO`
- [ ] T205 [P] [US3] Contract test `GET /alertas` and `PATCH /alertas/{id}/lido` in `backend/tests/contract/test_alertas.py`: filters, `total_nao_lidos`, 404 for another user's alert
- [ ] T206 [P] [US3] Integration test `backend/tests/integration/test_analise_alertas_flow.py`: an exceeded pilar creates 1 alert; re-analysis creates no duplicate (research R2); a changed amount updates it and resets `lido`; no alert when everything is within the limit (UC06 FA01)
- [ ] T207 [P] [US4] Integration test for the proactive trigger: a current-month expense that crosses the limit creates an alert; a past-month expense does not (research R3); user B's data is never included (SC-002 from 000)

## Phase 3: Core implementation

- [ ] T208 [P] [US1] Create `backend/app/domain/analise.py` with the `AnaliseFinanceira`, `DistribuicaoPilar` and `DadosInsuficientes` dataclasses and `calcular()` (makes T201 and T203 pass)
- [ ] T209 [P] [US2] Create `backend/app/domain/formatacao.py` (`format_brl`, `format_pct`, `format_data`) and `backend/app/domain/interpretacao.py` with the research R5 templates (makes T202 pass)
- [ ] T210 [US3] Create `backend/app/services/alerta_service.py`: `upsert_limite`, `listar` (with `total_nao_lidos`), `marcar_lido`
- [ ] T211 [US1] Create `backend/app/services/analise_service.py`: the aggregate query, then `calcular`, then alert upsert, then `interpretar`; plus `avaliar_alertas(usuario, hoje)`
- [ ] T212 [P] Create `backend/app/schemas/analise.py` and `backend/app/schemas/alerta.py` (Decimal → string serialization, discriminated union on `situacao`)
- [ ] T213 Create the routers `backend/app/api/routers/analise.py` and `alertas.py` and register them (makes T204–T206 pass)
- [ ] T214 [US4] Hook `analise_service.avaliar_alertas` into `movimentacao_service.cadastrar` and `categorizar` for current-month movements (makes T207 pass)

## Phase 4: Frontend

- [ ] T215 [P] Create `frontend/src/api/analise.ts` and `alertas.ts` (types plus hooks; registering a movement invalidates the analysis and alerts queries)
- [ ] T216 [P] [US1] Create `frontend/src/components/PeriodoSelector.tsx` (month prev/next, custom range)
- [ ] T217 [P] [US1] Create `frontend/src/components/PilarCard.tsx`: total, limit, an accessible progress bar (`role="progressbar"`, `aria-valuenow`), and a status label that does not rely on color alone
- [ ] T218 [US1] [US2] Create `frontend/src/pages/AnalisePage.tsx`: summary, 3 cards, interpretation items, exceeded banner, insufficient-data state
- [ ] T219 [US3] Create `frontend/src/pages/AlertasPage.tsx` and `frontend/src/components/AlertasBell.tsx` (unread badge in `Layout`)
- [ ] T220 [P] Component tests: PilarCard exceeded vs within, the AnalisePage insufficient-data state

## Phase 5: Polish

- [ ] T221 Run quickstart.md end to end and check 360 px
- [ ] T222 Resolve the NEEDS CLARIFICATION items (period, proactive trigger, Futuro semantics) and update spec, research and tests if the answers differ from the provisional defaults

## Dependencies

T200 → T201–T207 → T208/T209 → T210 → T211 → T212 → T213 → T214 → T215–T220 → T221–T222
