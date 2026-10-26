# Data Model: 004-recorrencias

Source: the Sprint 4 class diagram (`PagamentoRecorrente`, `IdentificadorRecorrencia`, `AlertaRecorrencia`, `Alerta`). Refinements are marked **Δ**.

## Enumerations

- `Frequencia` **Δ**: `SEMANAL` (7), `MENSAL` (30), `ANUAL` (365). Derived from `periodicidadeDias`, for display and projection (research R2, R3).
- `MotivoAlertaRecorrencia` **Δ**: `IDENTIFICADA` | `VENCIMENTO_PROXIMO` (research R4).

## Entities

### PagamentoRecorrente (`pagamento_recorrente`)
| Field | Type | Rules | Diagram |
|---|---|---|---|
| id | integer PK | | `id` |
| usuario_id | FK → usuario.id ON DELETE CASCADE | indexed | composition Usuario 1 — 0..* |
| descricao | varchar(200) | display name, from the most recent occurrence's description | `descricao` |
| descricao_normalizada **Δ** | varchar(200) | `UNIQUE(usuario_id, descricao_normalizada)` | grouping key |
| valor_medio | NUMERIC(12,2) | > 0 | `valorMedio` |
| periodicidade_dias | integer | 7, 30 or 365 | `periodicidadeDias` |
| frequencia **Δ** | varchar(7) | `Frequencia` (CHECK) | |
| ultima_ocorrencia **Δ** | date | | |
| proximo_vencimento | date | research R3 | `proximoVencimento` |
| qtd_ocorrencias **Δ** | integer | ≥ 2 | multiplicity 2..* |
| categoria_id **Δ** | FK → categoria.id, nullable | most frequent category in the group | |
| descartado **Δ** | boolean | default false (research R5) | |
| criado_em, atualizado_em | timestamp UTC | | |

**Derived (not stored):** `ativo = hoje − ultima_ocorrencia ≤ 2 × periodicidade_dias` (research R3).

**Operation:** `calcularProximoVencimento()` maps to `domain.recorrencia.projetar(ultima, frequencia, hoje)`.

### Movimentacao (changed)
- Add `pagamento_recorrente_id` (FK → pagamento_recorrente.id, nullable, ON DELETE SET NULL). This is the association `PagamentoRecorrente 0..1 → 2..* Movimentacao` (research R7).

### Alerta (changed): the AlertaRecorrencia columns
| Field | Type | Rules | Diagram |
|---|---|---|---|
| pagamento_recorrente_id | FK → pagamento_recorrente.id ON DELETE CASCADE, nullable | required when tipo = RECORRENCIA | `PagamentoRecorrente 1 → 0..* AlertaRecorrencia` |
| proximo_vencimento | date, nullable | required when tipo = RECORRENCIA | `AlertaRecorrencia.proximoVencimento` |
| motivo **Δ** | varchar(18), nullable | `MotivoAlertaRecorrencia` | |

**Constraints:**
- CHECK: `tipo <> 'RECORRENCIA' OR (pagamento_recorrente_id IS NOT NULL AND proximo_vencimento IS NOT NULL AND motivo IS NOT NULL)`
- Partial unique index on `(pagamento_recorrente_id, motivo) WHERE tipo='RECORRENCIA' AND motivo='IDENTIFICADA'`
- Partial unique index on `(pagamento_recorrente_id, motivo, proximo_vencimento) WHERE tipo='RECORRENCIA' AND motivo='VENCIMENTO_PROXIMO'`

**ORM:** `AlertaRecorrencia(Alerta)` with `polymorphic_identity="RECORRENCIA"`.

## Domain (pure) types (`backend/app/domain/recorrencia.py`)

| Type | Fields |
|---|---|
| `Candidato` | `chave`, `movimentacoes`, `frequencia`, `valor_medio`, `ultima_ocorrencia`, `proximo_vencimento`, `categoria_id` |
| `identificar(historico, hoje) -> list[Candidato]` | `IdentificadorRecorrencia.identificar()` in the diagram |
| `classificar(intervalos) -> Frequencia \| None` | research R2 |
| `valores_semelhantes(valores) -> bool` | research R2 |
| `projetar(ultima, frequencia, hoje) -> date` | research R3 |
