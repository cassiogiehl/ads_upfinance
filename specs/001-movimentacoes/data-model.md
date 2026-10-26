# Data Model: 001-movimentacoes

Source: the Sprint 4 class diagram (`Movimentacao`, `Categoria`, `TipoMovimentacao`, `Pilar`). `Usuario`, `Categoria` and the enums are defined in [000-foundation](../000-foundation/data-model.md).

## Movimentacao (`movimentacao`)

| Field | Type | Rules | Diagram |
|---|---|---|---|
| id | integer PK | | `id` |
| usuario_id | FK → usuario.id, ON DELETE CASCADE | required, indexed | composition Usuario 1 — 0..* |
| descricao | varchar(200) | required, trimmed, not blank | `descricao` |
| valor | NUMERIC(12,2) | required, CHECK `valor > 0` | `valor` |
| data | date | required (defaults to today, research R1) | `data` |
| tipo | varchar(7) | `ENTRADA` or `SAIDA` (CHECK) | `tipo` |
| categoria_id | FK → categoria.id | required | association 0..* — 1 |
| fatura_id | FK → fatura.id, nullable, ON DELETE SET NULL | added by migration in feature 003 | association Fatura 0..1 — 0..* |
| criado_em | timestamp UTC | default now | |

**Indexes:** `(usuario_id, data DESC)` for listing and period analysis. `(usuario_id, tipo, data)` for the analysis and recurrence features.

**Invariants (enforced in the service):**
- `categoria.tipo == movimentacao.tipo` (`CATEGORIA_INCOMPATIVEL`).
- A movement with `tipo = SAIDA` has a pilar, which is `categoria.pilar` (always set, by the 000 invariant).

## Derived operations (class diagram → Python)

| Diagram operation | Implementation |
|---|---|
| `Movimentacao.categorizar(Categoria c)` | `movimentacao_service.categorizar(db, usuario, mov_id, categoria_id)` |
| `Movimentacao.getPilar(): Pilar` | ORM property `pilar` → `self.categoria.pilar` |
| `Movimentacao.isSaida(): boolean` | ORM property `is_saida` |
| `Usuario.cadastrarMovimentacao(m)` | `movimentacao_service.cadastrar(db, usuario, dados)` |
| `Usuario.getMovimentacoes(periodo)` | `movimentacao_service.listar(db, usuario, inicio, fim, tipo, limit, offset)` |

## Response projection

`MovimentacaoOut` = `{id, descricao, valor (string), data, tipo, categoria: {id, nome}, pilar | null, fatura_id | null, criado_em}`
