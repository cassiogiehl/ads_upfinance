# Feature Specification: Identify recurring payments and alert the user

**Feature branch:** `004-recorrencias`
**Status:** Draft
**Depends on:** 001-movimentacoes, 002-analise-50-30-20 (alerts infrastructure). It benefits from 003 (more history).
**Sources:** RF010, RF011 · US08, US09 · UC09, UC10 · AD04 · Sprint 2 §10 · glossary examples (água, luz, internet)

## Overview

Rafael struggles to keep track of bills that repeat every month (Sprint 2 persona). With this feature the system looks through his expense history, recognizes payments that recur at a regular interval with a similar amount (for example water, electricity and internet), estimates the next due date and alerts him, so that recurring commitments don't catch him by surprise.

---

## User Scenarios & Testing

### User Story 1: Identify recurring payments from history (Priority: P1) · US08 · UC09 · RF010

As a user, I want the system to identify recurring payments in my history, so that I can keep track of bills that repeat over time.

**Independent test:** with three monthly "Internet Vivo" expenses of about R$ 120 on similar days, the recurrences screen lists "Internet Vivo" as monthly, with its next expected date.

**Acceptance scenarios** (Sprint 2 §10 US08)
1. **Given** SAIDA movements "Conta de luz" on 10/07, 09/08 and 11/09 of R$ 180, R$ 195 and R$ 172, **when** the history is analyzed, **then** a recurring payment "Conta de luz" is identified: monthly, average R$ 182,33, next due around 11/10.
2. **Given** only one occurrence of a description, **then** it is not identified as recurring. At least 2 occurrences are required (Sprint 4 multiplicity 2..*).
3. **Given** occurrences at irregular intervals (for example 3, 40 and 12 days apart), **then** no recurrence is identified (UC09 FA01).
4. **Given** occurrences with very different amounts (for example R$ 30 and R$ 900 at the same store), **then** no recurrence is identified.
5. **Given** descriptions that differ only in case, accents, dates or reference numbers ("CONTA LUZ 08/2026" and "Conta Luz 09/2026"), **then** they are treated as the same payment.
6. **Given** the user registers a new expense or confirms an invoice, **then** the history is re-analyzed automatically. The user can also ask for an analysis at any time.

### User Story 2: Be alerted about recurring payments (Priority: P1) · US09 · UC10 · RF011

As a user, I want to be alerted about identified recurring payments, so that I can follow their due dates.

**Acceptance scenarios** (Sprint 2 §10 US09)
1. **Given** a newly identified recurring payment, **then** the user receives an alert naming the payment, its average amount and its next expected date (UC10).
2. **Given** every alert, **then** it refers to one specific identified recurrence (Sprint 2 §10 US09 criterion 2).
3. **Given** no recurrence is identified, **then** no alert is issued (UC10 FA01).
4. **Given** a recurrence already identified, **when** the history is re-analyzed, **then** no duplicate "identified" alert is issued.

### User Story 3: Due-date reminder (Priority: P2) · US09 ("acompanhar seus vencimentos")

As a user, I want a reminder shortly before a recurring payment is expected, so that I don't forget it.

**Acceptance scenarios**
1. **Given** a monthly recurrence expected on 10/11, **when** the user uses the app on any day from 07/11 to 10/11, **then** they see one reminder alert for that due date.
2. **Given** the payment for that cycle has already been registered, **then** no reminder is shown and the next due date moves forward.

[NEEDS CLARIFICATION: how many days before the due date should the reminder appear? Provisional default: 3 days, see research R4.]

### User Story 4: View recurring payments (Priority: P2) · US08

As a user, I want to see all recurring payments and their next dates.

**Acceptance scenarios**
1. **Given** identified recurrences, **then** the list shows description, category, frequency (Mensal, Semanal, Anual), average amount, last occurrence and next expected date, ordered by next date.
2. **Given** one recurrence, **then** the user can see the movements it was based on.

### User Story 5: Dismiss a false positive (Priority: P3)

As a user, I want to mark an identified recurrence as "não é recorrente", so that it stops generating alerts.

[NEEDS CLARIFICATION: dismissing has no source in the sprints, but false positives are likely with a heuristic detector. Provisional default: included, see research R5.]

### Edge Cases

- A recurrence whose last occurrence is older than twice its interval (for example a cancelled subscription) is considered inactive. It produces no reminders and is listed separately.
- Monthly payments due on the 31st are projected to the last day of shorter months.
- Movements from different categories but with the same normalized description are still grouped. The recurrence shows the most frequent category.
- ENTRADA movements are never considered (RF010 talks about payments).

---

## Requirements

### Functional Requirements

- **FR-001:** The system MUST analyze the user's SAIDA movements from the last 12 months to identify recurring payments (RF010, UC09).
- **FR-002:** The system MUST group movements by normalized description (ignoring case, accents, digits and punctuation).
- **FR-003:** The system MUST identify a group as recurring only when it has ≥ 2 occurrences, all intervals fit one frequency (weekly, monthly or yearly) within tolerance, and amounts are similar. [NEEDS CLARIFICATION: interval and amount tolerances. Provisional defaults in research R2.]
- **FR-004:** The system MUST record, for each recurrence, its description, average amount, frequency in days, last occurrence and next expected date, plus the movements it is based on (Sprint 4 `PagamentoRecorrente`).
- **FR-005:** The system MUST re-run identification after a SAIDA movement is registered or recategorized, after an invoice is confirmed, and on demand.
- **FR-006:** The system MUST issue one alert when a recurrence is first identified (RF011, UC10), and no alert when none is identified (UC10 FA01).
- **FR-007:** The system SHOULD issue one reminder per due date within the reminder window (US3).
- **FR-008:** The system MUST list recurrences ordered by next expected date and show their source movements.
- **FR-009:** The system MAY let the user dismiss a recurrence, which suppresses its alerts and its re-identification (US5).

### Key Entities

- **PagamentoRecorrente:** a payment that repeats in the user's history: description, average amount, frequency in days, next due date, based on ≥ 2 movements.
- **AlertaRecorrencia:** an alert linked to one recurrence, with its next due date and its reason (newly identified, or due soon).

---

## Success Criteria

- **SC-001:** On a reference dataset (research R6), ≥ 90% of true recurring bills are identified and ≤ 10% of identified recurrences are false positives.
- **SC-002:** Identification for a user with 2,000 movements completes in under 1 second.
- **SC-003:** No duplicate alert is ever issued for the same recurrence, reason and due date (automated test).

## Traceability

| Spec item | Sprint source |
|---|---|
| US1, US4, FR-001…005, FR-008 | RF010, US08, UC09 (FA01), AD04, Sprint 4 `PagamentoRecorrente`, `IdentificadorRecorrencia` |
| US2, US3, FR-006, FR-007 | RF011, US09, UC10 (FA01), AD04, Sprint 4 `AlertaRecorrencia` |
| US5, FR-009 | No source. NEEDS CLARIFICATION |
