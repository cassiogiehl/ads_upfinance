# Tasks: 001-movimentacoes

**Input:** [plan.md](plan.md), [data-model.md](data-model.md), [contracts/openapi.yaml](contracts/openapi.yaml)
**Prerequisite:** 000-foundation is complete.
**Covers:** RF001, RF002, RF003, RF004 · UC01, UC02, UC03 · AD01 · RN002
**Legend:** `[P]` means it can run in parallel. `[USn]` is the story in `spec.md` (US1 = Sprint US01, US2 = US02, US3 = US03).

## Phase 1: Setup

- [ ] T100 Create the model `backend/app/models/movimentacao.py` per data-model.md, without `fatura_id` (added in 003), and the migration `backend/alembic/versions/0002_movimentacao.py` with its indexes

## Phase 2: Tests first (they must fail)

- [ ] T101 [P] [US1] Contract test `POST /movimentacoes` in `backend/tests/contract/test_movimentacoes.py`: 201 for ENTRADA and SAIDA, 422 `DADOS_INCOMPLETOS` listing the missing `campos` (UC01 FA01), 422 `VALOR_INVALIDO` for `0`, `-1`, `"abc"`, `"1.234"` and `"99999999999.00"` (UC01 FA02), 422 `CATEGORIA_INEXISTENTE`, 422 `CATEGORIA_INCOMPATIVEL`
- [ ] T102 [P] [US2] Contract test `PATCH /movimentacoes/{id}/categoria`: 200 with the new pilar, 422 `CATEGORIA_OBRIGATORIA` (UC02 FA01), 422 `CATEGORIA_INCOMPATIVEL`, 404 for an unknown id
- [ ] T103 [P] [US3] Contract test `GET /movimentacoes`: an empty list returns `{items: [], total: 0}` (UC03 FA01), newest-first order, filters `inicio`, `fim`, `tipo`, pagination
- [ ] T104 [P] [US1] Unit test the valor parsing and validation in `backend/tests/unit/test_movimentacao_validacao.py` (Decimal, > 0, ≤ 2 decimal places, maximum value)
- [ ] T105 [P] Integration test `backend/tests/integration/test_movimentacoes_flow.py`: register, then list, then recategorize. The pilar follows the category (Sprint 2 US02 "gasto contabilizado no pilar correspondente"). User B gets 404 on user A's movement and an empty list (SC-002)

## Phase 3: Core implementation

- [ ] T106 [P] Create `backend/app/schemas/movimentacao.py`: `MovimentacaoIn` (all fields optional), `MovimentacaoOut` (valor serialized as a string), `MovimentacaoPage`, `CategorizarIn`
- [ ] T107 [US1] Create `movimentacao_service.cadastrar` in `backend/app/services/movimentacao_service.py` with the validation order from plan.md, defaulting the date to today in America/Sao_Paulo (makes T101 and T104 pass)
- [ ] T108 [US2] Create `movimentacao_service.categorizar` (makes T102 pass)
- [ ] T109 [US3] Create `movimentacao_service.listar` and `obter`, scoped by `usuario_id` (makes T103 pass)
- [ ] T110 Create `backend/app/api/routers/movimentacoes.py` and register it (makes T105 pass)

## Phase 4: Frontend

- [ ] T111 [P] Create `frontend/src/lib/money.ts` (`parseBRL("1.500,00") → "1500.00"`, `formatBRL("1500.00") → "R$ 1.500,00"`) with unit tests
- [ ] T112 [P] Create `frontend/src/api/movimentacoes.ts`: typed client plus the hooks `useMovimentacoes(filters)`, `useCadastrarMovimentacao` and `useCategorizar` (invalidating the list)
- [ ] T113 [P] [US2] Create `frontend/src/components/PilarBadge.tsx` and `CategoriaSelect.tsx` (fetches by `tipo`, shows the pilar)
- [ ] T114 [US1] Create `frontend/src/components/MovimentacaoForm.tsx` and `pages/NovaMovimentacaoPage.tsx`: the ENTRADA/SAIDA toggle resets the category, error codes map to field messages
- [ ] T115 [US3] Create `frontend/src/pages/MovimentacoesPage.tsx`: responsive list/table, filters, empty state, inline category change
- [ ] T116 [P] Component tests for MovimentacaoForm (FA01/FA02 messages) and the MovimentacoesPage empty state

## Phase 5: Polish

- [ ] T117 Run quickstart.md and check the layout at 360 px
- [ ] T118 Record the answers to FR-009 and FR-010 (`/clarify`). If editing or deleting is approved, add stories and tasks here

## Dependencies

T100 → T101–T105 → T106 → T107–T109 → T110 → T111–T116 → T117–T118
