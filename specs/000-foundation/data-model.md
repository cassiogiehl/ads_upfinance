# Data Model: 000-foundation

Derived from the Sprint 4 class diagram (`Usuario`, `Categoria`, `Pilar`, `TipoMovimentacao`). Refinements are marked **Δ**.

## Enumerations

### Pilar
| Value | Percentual | Label (pt-BR) |
|---|---|---|
| `ESSENCIAL` | 0.50 | Essencial |
| `PESSOAL` | 0.30 | Pessoal |
| `FUTURO` | 0.20 | Futuro |

- Operation `calcular_limite(renda: Decimal) -> Decimal` returns `renda × percentual` (RN003).
- The percentages are fixed constants in code (RN004). They are not stored in the database. See Sprint 4 §3.4.

### TipoMovimentacao
`ENTRADA` | `SAIDA`. It is defined here because `Categoria` uses it (R2).

## Entities

### Usuario (`usuario`)
| Field | Type | Rules |
|---|---|---|
| id | integer PK | |
| nome | varchar(120) | required, trimmed, 1–120 characters |
| email | varchar(254) | required, unique, stored lowercase, valid email format |
| senha_hash | varchar(255) | argon2 hash. Never returned by the API |
| criado_em | timestamp (UTC) | default now |

Relationships (from the class diagram, implemented by later features): it owns 0..* `Movimentacao`, 0..* `Fatura`, 0..* `PagamentoRecorrente` and 0..* `Alerta`. All are deleted together with the user (cascade, because they are compositions).

### Categoria (`categoria`)
| Field | Type | Rules |
|---|---|---|
| id | integer PK | |
| nome | varchar(80) | required, unique |
| tipo **Δ** | varchar(7) | `ENTRADA` or `SAIDA` (CHECK) |
| pilar | varchar(9), nullable **Δ** | `ESSENCIAL`, `PESSOAL` or `FUTURO` (CHECK) |

Invariants:
- CHECK `(tipo = 'SAIDA' AND pilar IS NOT NULL) OR (tipo = 'ENTRADA' AND pilar IS NULL)`. This implements RN002 for spending categories. See research R2.
- The table is seeded by migration and has no write endpoints.

**Δ against Sprint 4:** `Categoria.pilar` was mandatory in the diagram. Income categories need no pilar, so `tipo` was added and `pilar` became conditional (research R2).
