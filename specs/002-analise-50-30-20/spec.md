# Feature Specification: 50-30-20 analysis and limit alerts

**Feature branch:** `002-analise-50-30-20`
**Status:** Draft
**Depends on:** 001-movimentacoes
**Sources:** RF005–RF007 · US04–US05 · UC04–UC06 · AD02 · RN001, RN003, RN004 · Sprint 2 §10

## Overview

Rafael can record his spending but cannot tell whether it is balanced (Sprint 2 persona). For a period, this feature shows how his expenses split across the pilares Essencial, Pessoal and Futuro, compares each one with its fixed limit (50%, 30% and 20% of his income), explains the result in plain language, and alerts him when a pilar exceeds its limit.

---

## User Scenarios & Testing

### User Story 1: See the 50-30-20 distribution (Priority: P1) · US04 · UC04 · RF005

As a user, I want to see how my expenses are distributed between Essencial, Pessoal and Futuro, so that I understand how my income is used.

**Independent test:** with seeded movements for one month, the analysis screen shows the 3 pilares with total, limit and percentage used.

**Acceptance scenarios** (Sprint 2 §10 US04)
1. **Given** in October an income of R$ 10.000,00 and expenses of Essencial R$ 4.000, Pessoal R$ 3.500 and Futuro R$ 1.000, **when** the user requests the October analysis, **then** the system shows:

   | Pilar | Total | Limite | % of limit used | Situação |
   |---|---|---|---|---|
   | Essencial | 4.000,00 | 5.000,00 | 80% | Dentro do limite |
   | Pessoal | 3.500,00 | 3.000,00 | 116,67% | Excedido |
   | Futuro | 1.000,00 | 2.000,00 | 50% | Dentro do limite |
2. **Given** any analysis, **then** the limits always use 50%, 30% and 20% of the period's income (RN001, RN004).
3. **Given** a period, **then** income is the sum of ENTRADA movements in that period, and each pilar total is the sum of SAIDA movements whose category belongs to that pilar.
4. **Given** a period with no movements, or with income = 0, **when** the analysis is requested, **then** the system says that financial records are needed for a complete analysis (UC04 FA01), and no distribution or alert is produced.

### User Story 2: Read an interpretation of my situation (Priority: P1) · US04 · UC05 · RF006

As a user, I want a plain-language interpretation of my distribution, so that I understand whether my spending is balanced.

**Acceptance scenarios**
1. **Given** the distribution from US1-1, **then** the interpretation states for each pilar whether it is within the limit (UC05 FA01) or exceeded and by how much (UC05 FA02). Example: "Seus gastos Pessoais ultrapassaram o limite em R$ 500,00 (116,67% do limite de 30%)."
2. **Given** all pilares within the limit, **then** the interpretation says the distribution follows the 50-30-20 rule.
3. **Given** the same data, **then** the interpretation is always identical: it is deterministic and rule-based, with no AI (RF006, Constitution II).
4. **Given** an analysis, **then** the interpretation also states the period's income, total expenses and the remaining balance (income − expenses).

### User Story 3: Receive a limit alert (Priority: P1) · US05 · UC06 · RF007

As a user, I want to be alerted when I exceed a pilar's limit, so that I know I need to rebalance.

**Acceptance scenarios** (Sprint 2 §10 US05)
1. **Given** the analysis in US1-1, **then** exactly one limit alert is generated, for Pessoal, stating the amount exceeded (R$ 500,00).
2. **Given** all pilares within the limit, **then** no alert is generated (UC06 FA01).
3. **Given** a pilar whose total equals its limit exactly, **then** it is *not* exceeded. "Ultrapassar" means strictly greater (RN003).
4. **Given** generated alerts, **when** the user opens the alerts list, **then** each alert shows its message, date and read state, and the user can mark it as read.
5. **Given** unread alerts, **then** the navigation shows the number of unread alerts.

### User Story 4: Proactive alert when registering an expense (Priority: P2) · US05

As a user, I want to be alerted as soon as an expense makes a pilar exceed its limit in the current month, without having to open the analysis.

**Acceptance scenarios**
1. **Given** a current-month Pessoal total of R$ 2.900 and an income of R$ 10.000, **when** the user registers a Pessoal expense of R$ 200, **then** a limit alert for Pessoal is generated.

[NEEDS CLARIFICATION: UC06 extends UC05, which is triggered by requesting the analysis, while US05 says "quando ultrapassar o limite". Is this proactive trigger wanted? Provisional default: yes, see research R3.]

### Edge Cases

- Income > 0 with no expenses: every pilar is 0 and within the limit, and the interpretation says so.
- Expenses exceed income: still analyzed. A negative remaining balance is highlighted.
- Movements dated outside the period are ignored.
- Running the same analysis repeatedly does not create duplicate alerts for the same pilar and period (research R2).
- The **Futuro** pilar is treated as a ceiling, like the others (RN003 applies to "determinado pilar"). [NEEDS CLARIFICATION: in the usual 50-30-20 guidance, Futuro is a savings *target* (at least 20%), not a ceiling. Should spending less than 20% on Futuro produce a warning, and should exceeding it still alert? Provisional default: follow RN003 literally.]

---

## Requirements

### Functional Requirements

- **FR-001:** The system MUST compute, for a period, the income (Σ ENTRADA) and the total SAIDA per pilar (RF005, RN002).
- **FR-002:** The system MUST compute each pilar's limit as income × fixed percentage, 50/30/20 (RN001, RN003, RN004).
- **FR-003:** The system MUST mark a pilar as exceeded when its total > limit (RN003).
- **FR-004:** The system MUST present, per pilar, the total, limit, % of limit used, % of income and situation (RF005).
- **FR-005:** The system MUST produce a deterministic textual interpretation from fixed templates (RF006).
- **FR-006:** The system MUST inform the user that more records are needed when the period has no movements or income = 0 (UC04 FA01).
- **FR-007:** The system MUST generate one limit alert per exceeded pilar per period, with the exceeded amount (RF007, UC06).
- **FR-008:** The system MUST NOT generate an alert when no pilar is exceeded (UC06 FA01).
- **FR-009:** The system MUST list the user's alerts and allow marking them as read.
- **FR-010:** The analysis period defaults to the current calendar month and can be changed to any date range. [NEEDS CLARIFICATION: is the period always a calendar month? The sprints say only "período". Provisional default in research R1.]

### Key Entities

- **AnaliseFinanceira:** the result for one period: income, generation time, three distributions and the interpretation. It is computed on request and not stored.
- **DistribuicaoPilar:** one pilar's total spent, limit and situation within an analysis.
- **Alerta / AlertaLimite:** a notification to the user with message, emission date and read state. A limit alert also records the pilar, the amount exceeded and the period.

---

## Success Criteria

- **SC-001:** The worked example in US1-1 produces exactly the table shown, verified by an automated test.
- **SC-002:** The analysis of a month with 500 movements is shown in under 1 second.
- **SC-003:** The same input always yields the same interpretation text (snapshot test).
- **SC-004:** In usability checks, a user can say which pilar is over its limit within 10 seconds of opening the analysis screen.

## Traceability

| Spec item | Sprint source |
|---|---|
| US1, FR-001…004, FR-006, FR-010 | RF005, US04, UC04 (FA01), AD02, RN001–RN004 |
| US2, FR-005 | RF006, US04, UC05 (FA01, FA02), AD02 |
| US3, US4, FR-007…009 | RF007, US05, UC06 (FA01), AD02 |
