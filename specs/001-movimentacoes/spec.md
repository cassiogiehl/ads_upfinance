# Feature Specification: Register, categorize and view movements

**Feature branch:** `001-movimentacoes`
**Status:** Draft
**Depends on:** 000-foundation
**Sources:** RF001–RF004 · US01–US03 · UC01–UC03 · AD01 · RN002 · Sprint 2 §10 acceptance criteria

## Overview

Rafael currently tracks money in a spreadsheet, forgets entries and updates everything by hand (Sprint 2 persona). This feature lets him record each income (entrada) or expense (saída) with a description, an amount, a date and a category. The category determines the pilar of the 50-30-20 rule. He can then review everything he has recorded. Every later analysis depends on this data.

---

## User Scenarios & Testing

### User Story 1: Register a movement (Priority: P1) · US01 · UC01 · RF001

As a user, I want to register an income or an expense, so that my financial control stays up to date.

**Independent test:** register one entrada and one saída, then see both in the list.

**Acceptance scenarios** (Sprint 2 §10 US01)
1. **Given** a signed-in user, **when** they register an ENTRADA "Salário outubro", R$ 5.000,00, category "Salário", **then** the movement is saved and appears in their list.
2. **Given** a signed-in user, **when** they register a SAIDA "Aluguel", R$ 1.500,00, category "Moradia", **then** the movement is saved with pilar Essencial.
3. **Given** the form, **when** descrição, valor, tipo or categoria is missing, **then** nothing is saved and the system asks for the missing information (UC01 FA01, code `DADOS_INCOMPLETOS`).
4. **Given** the form, **when** valor is zero, negative or not a number, **then** nothing is saved and the system asks the user to correct the amount (UC01 FA02, code `VALOR_INVALIDO`).
5. **Given** a saved movement, **then** it is immediately available for viewing (UC01 step 9).

### User Story 2: Categorize a movement (Priority: P1) · US02 · UC02 · RF002, RF003

As a user, I want to categorize my expenses, so that they are organized by pilar.

**Acceptance scenarios** (Sprint 2 §10 US02)
1. **Given** the registration form, **when** the user picks a type, **then** only categories from the system catalog that match that type are offered.
2. **Given** a SAIDA movement, **when** it is saved with a category, **then** the movement counts toward that category's pilar (RN002).
3. **Given** an existing movement, **when** the user changes its category, **then** the new category, and therefore the new pilar, is stored (UC02 main flow).
4. **Given** a change of category, **when** no category is selected, **then** the change is refused (UC02 FA01, code `CATEGORIA_OBRIGATORIA`).
5. **Given** a SAIDA movement, **when** the user tries to give it an ENTRADA category, or the reverse, **then** the change is refused (code `CATEGORIA_INCOMPATIVEL`).

### User Story 3: View movements (Priority: P1) · US03 · UC03 · RF004

As a user, I want to see my registered movements, so that I can follow my financial situation.

**Acceptance scenarios** (Sprint 2 §10 US03)
1. **Given** a user with movements, **when** they open the movements screen, **then** each movement shows descrição, valor, tipo, categoria, pilar and data (UC03 step 4).
2. **Given** a list, **then** the values shown match exactly what was registered, with 2 decimal places in Brazilian currency format.
3. **Given** a user with no movements, **when** they open the screen, **then** the system says there are no movements yet and offers to register one (UC03 FA01).
4. **Given** many movements, **then** they are ordered newest first, and the user can restrict the list to a date range and a type.
5. **Given** two users, **then** each sees only their own movements.

### Edge Cases

- valor with more than 2 decimal places is refused with `VALOR_INVALIDO`. It is not silently rounded.
- valor above R$ 9.999.999.999,99 (the storage limit) is refused with `VALOR_INVALIDO`.
- descrição made only of spaces counts as missing (`DADOS_INCOMPLETOS`).
- A category id that doesn't exist is refused with `CATEGORIA_INEXISTENTE`.
- Accessing another user's movement returns not found.

---

## Requirements

### Functional Requirements

- **FR-001:** The system MUST allow registering a movement with descrição, valor, tipo (ENTRADA/SAIDA), categoria and data (RF001).
- **FR-002:** The system MUST refuse a movement with any required field missing, and identify the missing fields (UC01 FA01).
- **FR-003:** The system MUST refuse valor ≤ 0, non-numeric valor, or valor with more than 2 decimal places (UC01 FA02).
- **FR-004:** The system MUST allow only system-provided categories whose type matches the movement type (RF002, RN002).
- **FR-005:** The system MUST derive the movement's pilar from its category and never accept a pilar directly (RF003, RN002).
- **FR-006:** The system MUST allow changing the category of an existing movement (UC02).
- **FR-007:** The system MUST list the user's movements newest first, with optional filters by date range and type (RF004, UC03).
- **FR-008:** The system MUST show an empty-state message when there are no movements (UC03 FA01).
- **FR-009:** The data defaults to today when not given. [NEEDS CLARIFICATION: should the user always enter the date explicitly? The sprints don't state it, but analysis by period (AD02) and recurrence detection (AD04) both require a date. Provisional default in research R1.]
- **FR-010:** [NEEDS CLARIFICATION: can a user edit the other fields or delete a movement? The sprints only define categorization (UC02). Provisional: not in v1, see research R2.]

### Key Entities

- **Movimentacao:** an income or an expense of one user, with descrição, valor (positive), data, tipo and exactly one categoria. It may have come from an invoice (feature 003).
- **Categoria / Pilar:** see 000-foundation.

---

## Success Criteria

- **SC-001:** A user can register a movement in under 30 seconds, using at most 5 form interactions.
- **SC-002:** 100% of saved SAIDA movements have exactly one pilar.
- **SC-003:** The movements list loads in under 1 second for 1,000 movements.
- **SC-004:** Every FA of UC01–UC03 has an automated test.

## Traceability

| Spec item | Sprint source |
|---|---|
| US1, FR-001…003, FR-009 | RF001, US01, UC01 (FA01, FA02), AD01 |
| US2, FR-004…006 | RF002, RF003, RN002, US02, UC02 (FA01), AD01 |
| US3, FR-007, FR-008 | RF004, US03, UC03 (FA01) |
