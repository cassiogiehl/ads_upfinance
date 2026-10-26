# Feature Specification: Foundation (user account and category catalog)

**Feature branch:** `000-foundation`
**Status:** Draft
**Sources:** Sprint 3 §2.1 (actor Usuário), Sprint 4 §3.1 (`Usuario`, `Categoria`, `Pilar`), RF003, RN002, RNF001, RNF002

## Overview

Every UPFinance capability belongs to a single user and depends on a fixed catalog of categories, each tied to a pilar of the 50-30-20 rule. This feature provides both: a person can create an account, sign in and reach the application from any browser, and the system exposes the categories that the later features use.

Authentication is not described in Sprints 2–4. It is required because the class diagram makes `Usuario` the owner of all data (compositions), and the application is Web-accessible (RNF001). The decision is recorded in `research.md` (R1).

---

## User Scenarios & Testing

### User Story 1: Create an account (Priority: P1)

As a new user, I want to create an account with my name, email and password, so that my financial data is kept private to me.

**Why this priority:** every other feature requires an owner for its data.

**Independent test:** register, then sign in with the same credentials.

**Acceptance scenarios**
1. **Given** no account exists for `rafael@example.com`, **when** the visitor registers with name "Rafael", that email and a valid password, **then** the account is created and the user is signed in.
2. **Given** an account already exists for `rafael@example.com`, **when** someone registers with the same email, **then** registration is refused with the message "Este e-mail já está cadastrado".
3. **Given** the registration form, **when** name, email or password is missing, or the email is malformed, **then** registration is refused and the invalid fields are identified.

### User Story 2: Sign in and sign out (Priority: P1)

As a registered user, I want to sign in and out, so that only I can see my data.

**Acceptance scenarios**
1. **Given** a registered user, **when** they sign in with the correct email and password, **then** they reach the home screen.
2. **Given** a registered user, **when** they sign in with a wrong password, **then** access is refused with a generic message that does not reveal whether the email exists.
3. **Given** a signed-in user, **when** they sign out, **then** protected screens are no longer accessible without signing in again.
4. **Given** a visitor who is not signed in, **when** they open a protected screen, **then** they are redirected to sign-in.

### User Story 3: See the category catalog (Priority: P1)

As a user, I want to see the categories available and which pilar each one belongs to, so that I can classify my movements correctly (RF003, RN002).

**Acceptance scenarios**
1. **Given** a signed-in user, **when** they request the categories, **then** every category is listed with exactly one pilar: Essencial, Pessoal or Futuro.
2. **Given** the catalog, **then** every pilar has at least one category.
3. **Given** a user, **then** categories cannot be created, edited or deleted. They are provided by the system (RN002, Sprint 2 US02 criterion "categoria disponibilizada pelo sistema").

### User Story 4: Use the app on phone and desktop (Priority: P2)

As a user, I want to use UPFinance from a desktop or mobile browser (RNF001, RNF002).

**Acceptance scenarios**
1. **Given** a 360 px wide screen, **when** any screen of the application is opened, **then** all content is usable without horizontal scrolling.
2. **Given** a desktop browser, **then** the same features are available.

### Edge Cases

- An email that differs only in letter case is treated as the same email.
- Leading and trailing spaces in name and email are ignored.
- An expired session sends the user back to sign-in without losing the screen they were on.

---

## Requirements

### Functional Requirements

- **FR-001:** The system MUST allow a visitor to register with name, email and password.
- **FR-002:** The system MUST reject a registration whose email already exists (case-insensitive).
- **FR-003:** The system MUST authenticate users by email and password and keep them signed in for a session.
- **FR-004:** The system MUST restrict all financial data to the signed-in user who owns it (Constitution V).
- **FR-005:** The system MUST provide a fixed catalog of categories, each associated with exactly one pilar (RF003, RN002).
- **FR-006:** The system MUST expose the pilares Essencial (50%), Pessoal (30%) and Futuro (20%) as fixed values (RN001, RN004).
- **FR-007:** The interface MUST be usable in desktop and mobile browsers (RNF001, RNF002).
- **FR-008:** Passwords MUST have at least 8 characters. They MUST never be stored or displayed in readable form.

### Key Entities

- **Usuario:** the person using the application. Has a name, a unique email and credentials. Owns all financial records.
- **Categoria:** a system-provided classification with a name, belonging to one pilar.
- **Pilar:** a fixed value (Essencial, Pessoal or Futuro) with a fixed percentage (50 / 30 / 20).

---

## Success Criteria

- **SC-001:** A new user can register and reach the home screen in under 1 minute.
- **SC-002:** No request made by one user can return another user's data. This is verified by an automated cross-user test for every resource.
- **SC-003:** 100% of catalog categories map to exactly one pilar, and each pilar has at least one category.
- **SC-004:** All screens pass a manual check at widths of 360 px and 1280 px.

## Traceability

| Item | Source |
|---|---|
| US1, US2, FR-001…FR-004, FR-008 | Sprint 3 §2.1 (single actor Usuário); Sprint 4 `Usuario` compositions. Auth decision in research R1 |
| US3, FR-005, FR-006 | RF003, RN001, RN002, RN004; Sprint 4 `Categoria`, `Pilar` |
| US4, FR-007 | RNF001, RNF002 |
