# Tasks: 003-fatura-pdf

**Input:** [plan.md](plan.md), [data-model.md](data-model.md), [contracts/openapi.yaml](contracts/openapi.yaml)
**Prerequisite:** 001-movimentacoes is complete (002 recommended).
**Covers:** RF008, RF009 · UC07, UC08 · AD03
**Legend:** `[P]` means it can run in parallel. US1 = Sprint US06, US2/US3 = Sprint US07, US4 = history.

## Phase 1: Setup

- [ ] T300 Add `pdfplumber` and `python-multipart` to the runtime dependencies and `reportlab` to the dev dependencies in `backend/pyproject.toml`
- [ ] T301 Create `backend/app/models/fatura.py` (`Fatura`, `ItemFatura`, with the model methods `marcar_interpretada` and `marcar_falha`), add `fatura_id` to `Movimentacao`, and create the migration `0004_fatura.py`
- [ ] T302 [P] Create `backend/tests/fixtures/gerar_faturas.py`: reportlab builders for the generic, year-rollover, with-payments, installment, empty, image-only and encrypted PDFs (research R8), exposed as pytest fixtures and as a CLI (quickstart)

## Phase 2: Tests first (they must fail)

- [ ] T303 [P] [US2] Unit tests in `backend/tests/unit/test_fatura_parsing.py`: `parse_valor_brl("1.234,56") == Decimal("1234.56")`, `parse_data_linha("12/10")` and `("12 OUT")`, `inferir_ano` across December/January (research R4), `deve_ignorar` for payments, refunds and negative amounts (research R5), `normalizar_descricao` (accents, `*`, `PARC 03/10`)
- [ ] T304 [P] [US2] Unit tests in `backend/tests/unit/test_interpretador_generico.py`: `suporta()` is true for the generic fixture and false for the empty one; `interpretar()` returns the exact expected items for each fixture; an installment line keeps its marker in the description
- [ ] T305 [P] [US2] Unit tests in `backend/tests/unit/test_sugestao.py`: a keyword match; history takes precedence over keywords; no match gives `None`
- [ ] T306 [P] [US1] Contract test `POST /faturas` in `backend/tests/contract/test_faturas.py`: 201 INTERPRETADA with items; 201 NAO_INTERPRETADA for the empty, image-only and encrypted fixtures (UC08 FA01); 415 for a renamed `.jpg` (UC07 FA01); 413 above 10 MB; 409 for a duplicate
- [ ] T307 [P] [US3] Contract test `POST /faturas/{id}/confirmar`: 200 with the created count; 422 `CATEGORIA_OBRIGATORIA` with `details.itens`; 422 `NENHUM_ITEM_INCLUIDO`; 409 on a second confirmation; 409 for a NAO_INTERPRETADA invoice; 404 for another user's invoice
- [ ] T308 [P] [US3] Integration test `backend/tests/integration/test_fatura_flow.py`: upload, adjust, confirm. The SAIDA movements have `fatura_id`, excluded items create nothing (SC-004), the analysis totals include the imported items, and a failure halfway through confirmation rolls everything back

## Phase 3: Core implementation

- [ ] T309 [P] [US2] Create `backend/app/fatura/parsing.py` and `normalizacao.py` (makes T303 pass)
- [ ] T310 [P] [US2] Create `backend/app/fatura/tipos.py` and `documento.py` (`DocumentoPDF.abrir(bytes)`, which raises `PdfIlegivel` for encrypted or corrupt files)
- [ ] T311 [US2] Create `backend/app/fatura/interpretadores/generico.py` (`InterpretadorFaturaPDF`) and `registry.py` (makes T304 pass)
- [ ] T312 [P] [US2] Create `backend/app/fatura/sugestao.py` with the keyword table and history lookup (makes T305 pass)
- [ ] T313 [US1] Create `fatura_service.enviar` in `backend/app/services/fatura_service.py`: chunked size check, magic bytes, sha256 duplicate check, parse, interpret, suggest, persist
- [ ] T314 [US3] Create `fatura_service.confirmar`: apply the adjustments, validate, create the movements in one transaction, set CONFIRMADA, then call `analise_service.avaliar_alertas` for each affected month
- [ ] T315 [US4] Create `fatura_service.listar` and `obter` (with counts)
- [ ] T316 [P] Create `backend/app/schemas/fatura.py`
- [ ] T317 Create `backend/app/api/routers/faturas.py` and register it (makes T306–T308 pass)

## Phase 4: Frontend

- [ ] T318 [P] Create `frontend/src/api/faturas.ts` (multipart upload with `FormData`, typed responses)
- [ ] T319 [US1] Create `frontend/src/pages/EnviarFaturaPage.tsx`: picker and drop zone, upload progress, FA01 messages for UC07 and UC08, retry without leaving the page
- [ ] T320 [US2] [US3] Create `frontend/src/pages/RevisarFaturaPage.tsx`: responsive table/cards, include toggles, `CategoriaSelect` pre-filled with a "sugerida" tag, live total, confirm button with server-error highlighting
- [ ] T321 [P] [US4] Create `frontend/src/pages/FaturasPage.tsx` (history with status badges) and add the routes `/faturas`, `/faturas/enviar` and `/faturas/:id/revisar`
- [ ] T322 [P] Component tests for RevisarFaturaPage (confirm disabled while a category is missing, total recalculated when items are excluded)

## Phase 5: Polish

- [ ] T323 Collect real anonymized invoices for each target bank (FR-010) into `backend/tests/fixtures/faturas/real/` (git-ignored) and measure SC-001. Add bank-specific interpreters if extraction is below 95%
- [ ] T324 Run quickstart.md end to end and check 360 px

## Dependencies

T300 → T301/T302 → T303–T308 → T309/T310 → T311/T312 → T313 → T314/T315 → T316 → T317 → T318–T322 → T323–T324
