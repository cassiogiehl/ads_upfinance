# Feature Specification: Upload and interpret a credit-card invoice (PDF)

**Feature branch:** `003-fatura-pdf`
**Status:** Draft
**Depends on:** 001-movimentacoes (002 is optional: alerts are re-evaluated after import)
**Sources:** RF008, RF009 · US06, US07 · UC07, UC08 · AD03 · Sprint 2 §10 and the risk note on PDF formats

## Overview

Registering every card purchase by hand is the most tedious part of Rafael's routine. With this feature he can upload his card invoice as a PDF. The system reads the purchases, suggests a category for each one, and lets him review and adjust them. Only after he confirms are they recorded as expenses.

Invoice layouts vary across banks, and this is a known project risk (Sprint 2, Sprint 3 UC08). The user review step (AD03) and the pluggable interpreters (Sprint 4 `InterpretadorFatura`) are how this spec mitigates it.

---

## User Scenarios & Testing

### User Story 1: Upload an invoice (Priority: P1) · US06 · UC07 · RF008

As a user, I want to upload my card invoice in PDF format, so that I don't have to type every card expense.

**Independent test:** upload a supported PDF and see the extracted items on a review screen.

**Acceptance scenarios** (Sprint 2 §10 US06)
1. **Given** a signed-in user with a PDF invoice, **when** they select and send the file, **then** the system receives it and passes it to interpretation (UC07 steps 1–5).
2. **Given** a file that is not a PDF (for example `.jpg` or `.xlsx`, or a file renamed to `.pdf`), **when** it is sent, **then** the system refuses it and asks for a PDF invoice (UC07 FA01). The user can choose another file without leaving the screen (AD03 loop).
3. **Given** a file over the size limit, **then** it is refused with a clear message.
4. **Given** that uploading is optional (RF008), **then** the user can use every other feature without ever uploading an invoice.

### User Story 2: Interpret the invoice and review the items (Priority: P1) · US07 · UC08 · RF009

As a user, I want the system to read my invoice, so that I get my expenses without registering everything manually.

**Acceptance scenarios** (Sprint 2 §10 US07)
1. **Given** a PDF in a supported layout, **when** it is interpreted, **then** every purchase line is extracted with date, description and amount (AD03 "Identificar gastos *").
2. **Given** the extracted items, **then** each one has a suggested spending category, or none when no suggestion applies.
3. **Given** the review screen, **then** the user can change the category of any item and exclude items they don't want to import.
4. **Given** a PDF whose layout is not recognized, or from which no purchase can be extracted, **then** the system says the invoice could not be interpreted (UC08 FA01), and no movement is created.
5. **Given** payment, credit or refund lines on the invoice (negative amounts, "pagamento recebido", "estorno"), **then** they are not extracted as expenses.

### User Story 3: Confirm and record the expenses (Priority: P1) · US07 · UC08 step 5

As a user, I want to confirm the reviewed items, so that they become part of my financial control.

**Acceptance scenarios**
1. **Given** a reviewed invoice, **when** the user confirms, **then** each included item becomes a SAIDA movement with its date, description, amount and category, linked to the invoice (Sprint 4 `Fatura 0..1 → 0..* Movimentacao`).
2. **Given** an included item without a category, **when** the user confirms, **then** confirmation is refused, and the items that need a category are highlighted (`CATEGORIA_OBRIGATORIA`).
3. **Given** an invoice already confirmed, **then** it cannot be confirmed again.
4. **Given** confirmed movements, **then** they appear in the movements list and count in the 50-30-20 analysis like any other expense.

### User Story 4: Invoice history (Priority: P3)

As a user, I want to see the invoices I uploaded and their status, so that I know which ones I have already imported.

**Acceptance scenarios**
1. **Given** uploaded invoices, **then** the list shows file name, upload date, status (Recebida, Interpretada, Não interpretada, Confirmada) and the number of items and movements.

### Edge Cases

- Uploading the exact same file twice is refused with "Esta fatura já foi enviada" (prevents double counting).
- Password-protected or corrupted PDFs are treated as "não pôde ser interpretada" (UC08 FA01).
- Scanned or image-only PDFs, which contain no text, are treated the same way. OCR is out of scope.
- Purchase lines usually lack a year. The year is inferred from the invoice due or closing date (research R4).
- Installment purchases ("PARC 03/10") are imported as a single expense for the installment amount, keeping the installment marker in the description.
- International purchases use the BRL amount shown on the invoice.

---

## Requirements

### Functional Requirements

- **FR-001:** The system MUST allow uploading one PDF file per request, up to 10 MB (RF008, UC07).
- **FR-002:** The system MUST check that the file really is a PDF by its content, not only its name, and otherwise refuse it (UC07 FA01).
- **FR-003:** The system MUST extract date, description and amount of each purchase line from supported layouts (RF009, UC08).
- **FR-004:** The system MUST mark an invoice as not interpretable when no supported layout matches or no purchases are found (UC08 FA01).
- **FR-005:** The system MUST suggest a category for each item using deterministic rules: keyword rules first, then the user's own past categorization of a similar description. No AI (Constitution II).
- **FR-006:** The system MUST let the user review, recategorize and exclude items before anything is recorded (AD03).
- **FR-007:** The system MUST create one SAIDA movement per included item on confirmation, linked to the invoice, in a single all-or-nothing operation.
- **FR-008:** The system MUST prevent confirming the same invoice twice, and uploading the same file twice.
- **FR-009:** The set of supported layouts MUST be extensible without changing the rest of the system (Sprint 4 §3.4, `InterpretadorFatura`).
- **FR-010:** [NEEDS CLARIFICATION: which banks' invoice layouts must v1 support? The sprints say "formatos contemplados pelo projeto" without listing them. Provisional default: one generic line-pattern interpreter (research R2), validated against real invoices that the team provides.]

### Key Entities

- **Fatura:** an uploaded invoice file, with file name, upload date, status and a fingerprint to detect duplicates.
- **ItemFatura:** a purchase extracted from an invoice and awaiting review: date, description, amount, suggested category, chosen category, include flag.
- **InterpretadorFatura:** a reader for one invoice layout. It can tell whether it supports a file, and extracts its items.

---

## Success Criteria

- **SC-001:** For each supported layout, ≥ 95% of purchase lines in the reference invoices are extracted with the correct date, description and amount.
- **SC-002:** Uploading and interpreting a typical (≤ 5 pages) invoice takes under 5 seconds.
- **SC-003:** A user can import a 30-line invoice, review it and confirm it in under 3 minutes.
- **SC-004:** 0 movements are created from an invoice that the user did not confirm.

## Traceability

| Spec item | Sprint source |
|---|---|
| US1, FR-001, FR-002 | RF008, US06, UC07 (FA01), AD03 |
| US2, FR-003…006, FR-009, FR-010 | RF009, US07, UC08 (FA01), AD03, Sprint 4 `InterpretadorFatura` |
| US3, FR-007, FR-008 | RF009, US07 ("gastos identificados devem poder ser utilizados no controle financeiro"), AD03 "Registrar gastos como movimentações de saída" |
| US4 | Sprint 4 `Usuario 1 *— 0..* Fatura`, `StatusFatura` |
