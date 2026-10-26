# Research: 001-movimentacoes

## R1: Movement date (FR-009)

- **Status:** provisional default, pending the clarification in spec FR-009.
- **Decision:** `data` is an optional input that defaults to today in America/Sao_Paulo. The form pre-fills today and the user can change it. Future dates are allowed, so expected bills can be recorded.
- **Rationale:** `data` exists in the Sprint 4 class diagram, and AD02 (period analysis) and AD04 (interval between dates) need it. Pre-filling keeps UC01 as listed (descrição, valor, tipo, categoria) while still capturing the date.

## R2: Editing and deleting movements (FR-010)

- **Status:** provisional default, pending the clarification in spec FR-010.
- **Decision:** v1 offers only category changes (UC02). There is no general edit and no delete.
- **Rationale:** Constitution I says not to add behavior without a source. If the product owner approves editing and deleting, a new story adds `PATCH /movimentacoes/{id}` and `DELETE /movimentacoes/{id}`. The data model already supports both.
- **Risk:** without delete, a user cannot fix a duplicate. Raise this in `/clarify`.

## R3: Mapping alternative flows to error codes

| Flow | Condition | HTTP | `code` |
|---|---|---|---|
| UC01 FA01 | descrição, valor, tipo or categoria_id missing or blank | 422 | `DADOS_INCOMPLETOS` (`details.campos: [...]`) |
| UC01 FA02 | valor ≤ 0, not numeric, more than 2 decimal places, or too large | 422 | `VALOR_INVALIDO` |
| UC02 FA01 | `categoria_id` missing on a category change | 422 | `CATEGORIA_OBRIGATORIA` |
| (derived) | category type ≠ movement type | 422 | `CATEGORIA_INCOMPATIVEL` |
| (derived) | category id unknown | 422 | `CATEGORIA_INEXISTENTE` |
| UC03 FA01 | no movements | 200 with an empty `items` list | (the UI shows the empty state) |

- **Decision:** the request schemas declare these fields as optional. `movimentacao_service` validates them in a fixed order (completeness, then valor, then categoria), so each FA produces its own code instead of a generic Pydantic 422.
- **Rationale:** stable codes per FA make the traceability testable (Constitution III).

## R4: Representing money in JSON

- **Decision:** `valor` travels as a decimal **string** (`"1500.00"`) in both requests and responses. The API also accepts numbers in requests. The frontend formats with `Intl.NumberFormat('pt-BR', {style:'currency', currency:'BRL'})`.
- **Rationale:** this avoids float rounding in JavaScript (Constitution IV).

## R5: Pagination

- **Decision:** offset pagination (`limit` defaults to 50 with a maximum of 200, plus `offset`). The response is `{items, total}`.
- **Rationale:** simple, and enough for the volume of a personal finance app.
