# Tasks: 004-recorrencias

**Input:** [plan.md](plan.md), [data-model.md](data-model.md), [contracts/openapi.yaml](contracts/openapi.yaml)
**Prerequisite:** 001 and 002 are complete (003 is optional, since the hook into `fatura_service` applies only if it exists).
**Covers:** RF010, RF011 · UC09, UC10 · AD04
**Legend:** `[P]` means it can run in parallel. US1/US4 = Sprint US08, US2/US3 = Sprint US09, US5 = dismissal.

## Phase 1: Setup

- [ ] T400 Add `python-dateutil` to `backend/pyproject.toml`. If 003 is not built yet, create `backend/app/fatura/normalizacao.py` with `normalizar_descricao` and its unit tests (see 003 research R6 and this feature's research R1)
- [ ] T401 Create `backend/app/models/pagamento_recorrente.py`, add `AlertaRecorrencia` to `backend/app/models/alerta.py`, add `pagamento_recorrente_id` to `Movimentacao`, and create the migration `0005_recorrencia.py` with its constraints and partial unique indexes (data-model.md)
- [ ] T402 [P] Create `backend/tests/fixtures/historico_recorrencias.py`: the 12-month reference dataset with its expected recurrences (research R6)

## Phase 2: Tests first (they must fail)

- [ ] T403 [P] [US1] Unit tests in `backend/tests/unit/test_recorrencia_dominio.py`:
  - `classificar([30, 33]) == MENSAL`, `classificar([3, 40]) is None`, the weekly and yearly bands
  - `valores_semelhantes([180, 195, 172])` is True and `([30, 900])` is False
  - `projetar` from 31/01 gives 28/02 (or 29/02), and dates in the past keep advancing to ≥ today
  - `identificar` on the spec US1-1 example gives MENSAL, an average of `182.33` and a next date of 11/10
  - a single occurrence gives nothing; ENTRADA is ignored; the same-day duplicate counts once
- [ ] T404 [P] [US1] Precision and recall test in `backend/tests/unit/test_recorrencia_dataset.py` on the reference dataset: recall ≥ 0.9 and precision ≥ 0.9 (SC-001); 2,000 movements processed in under 1 s (SC-002)
- [ ] T405 [P] [US1] [US4] Contract test in `backend/tests/contract/test_recorrencias.py` for `POST /recorrencias/identificar` (`novas` and `atualizadas`; an empty result for UC09 FA01), `GET /recorrencias` (the `situacao` filter, ordered by `proximo_vencimento`), `GET /recorrencias/{id}` (≥ 2 movements), `PATCH` (dismiss), and 404 for another user's recurrence
- [ ] T406 [P] [US2] [US3] Integration test in `backend/tests/integration/test_recorrencias_flow.py`:
  - registering the 2nd monthly expense creates a recurrence and exactly 1 `IDENTIFICADA` alert (UC10)
  - re-running creates no duplicate (SC-003)
  - no recurrence means no alert (UC10 FA01)
  - with a frozen `hoje`, a recurrence due in 2 days produces 1 `VENCIMENTO_PROXIMO` alert on `GET /alertas`, and repeated calls create no duplicate
  - registering the cycle's payment advances `proximo_vencimento`
  - a dismissed recurrence produces no alerts and its unread alerts are marked as read (US5)

## Phase 3: Core implementation

- [ ] T407 [US1] Create `backend/app/domain/recorrencia.py` with `Frequencia`, `Candidato`, `classificar`, `valores_semelhantes`, `projetar` and `identificar` (makes T403 and T404 pass)
- [ ] T408 [US1] Create `recorrencia_service.identificar_para(db, usuario, hoje)` in `backend/app/services/recorrencia_service.py`: query, then `identificar`, then upsert (plan.md rules), then re-link the movements' FKs, then IDENTIFICADA alerts for new recurrences
- [ ] T409 [US3] Create `recorrencia_service.gerar_lembretes(db, usuario, hoje)`, and add `alerta_service.criar_recorrencia` with deduplication. `alerta_service.listar` calls `gerar_lembretes` first
- [ ] T410 [US4] [US5] Create `recorrencia_service.listar(situacao)`, `obter(id)` and `descartar(id, flag)`, where dismissal marks the unread alerts as read
- [ ] T411 [P] Create `backend/app/schemas/recorrencia.py` (`ativo` and `dias_para_vencimento` computed against `hoje`)
- [ ] T412 Create `backend/app/api/routers/recorrencias.py` and register it. `GET /recorrencias` calls `gerar_lembretes` first (makes T405 pass)
- [ ] T413 [US1] Hook `identificar_para` into `movimentacao_service.cadastrar` and `categorizar` (SAIDA) and into `fatura_service.confirmar` if 003 exists (makes T406 pass)

## Phase 4: Frontend

- [ ] T414 [P] Create `frontend/src/api/recorrencias.ts` (types plus hooks; registering a movement invalidates the recurrences and alerts queries)
- [ ] T415 [P] [US4] Create `frontend/src/components/RecorrenciaCard.tsx`: frequency label, average amount, next date, "vence em N dias" highlighted when ≤ 3, expandable list of movements, and a "Não é recorrente" action
- [ ] T416 [US1] [US4] Create `frontend/src/pages/RecorrenciasPage.tsx` with tabs (Ativos, Inativos, Descartados), the "Analisar histórico agora" button and the UC09 FA01 empty state. Add the `/recorrencias` route
- [ ] T417 [US2] [US3] Extend `frontend/src/pages/AlertasPage.tsx` to render RECORRENCIA alerts (icon, link to the recurrence)
- [ ] T418 [P] Component tests for RecorrenciaCard (due-soon highlight, the dismiss action)

## Phase 5: Polish

- [ ] T419 Run quickstart.md end to end and check 360 px
- [ ] T420 Resolve the NEEDS CLARIFICATION items (tolerances, reminder window, dismissal) and adjust research R2, R4 and R5 and the tests if the answers differ from the defaults

## Dependencies

T400 → T401/T402 → T403–T406 → T407 → T408 → T409/T410 → T411 → T412 → T413 → T414–T418 → T419–T420
