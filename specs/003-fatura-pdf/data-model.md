# Data Model: 003-fatura-pdf

Source: the Sprint 4 class diagram (`Fatura`, `StatusFatura`, `InterpretadorFatura`, `InterpretadorFaturaPDF`, association `Fatura 0..1 → 0..* Movimentacao`). Refinements are marked **Δ**.

## Enumerations

### StatusFatura
`RECEBIDA` → `INTERPRETADA` | `NAO_INTERPRETADA`; `INTERPRETADA` → `CONFIRMADA` **Δ** (research R7).

## Entities

### Fatura (`fatura`)
| Field | Type | Rules | Diagram |
|---|---|---|---|
| id | integer PK | | `id` |
| usuario_id | FK → usuario.id ON DELETE CASCADE | indexed | composition Usuario 1 — 0..* |
| nome_arquivo | varchar(255) | required, original file name with the path stripped | `nomeArquivo` |
| data_envio | timestamp UTC | default now | `dataEnvio` (refined from date to timestamp) |
| status | varchar(16) | StatusFatura (CHECK) | `status` |
| sha256 **Δ** | char(64) | unique per user: `UNIQUE(usuario_id, sha256)` | research R3 |
| interpretador **Δ** | varchar(50), nullable | name of the interpreter used | |
| motivo_falha **Δ** | varchar(255), nullable | set when NAO_INTERPRETADA | `marcarFalha(motivo)` |
| data_referencia **Δ** | date, nullable | inferred due or closing date (research R4) | |
| confirmada_em **Δ** | timestamp, nullable | | |

### ItemFatura (`item_fatura`) **Δ**
This is a new class: the draft purchase between interpretation and confirmation (the AD03 review step).

| Field | Type | Rules |
|---|---|---|
| id | integer PK | |
| fatura_id | FK → fatura.id ON DELETE CASCADE | indexed |
| ordem | integer | position on the invoice |
| data | date | required |
| descricao | varchar(200) | required |
| valor | NUMERIC(12,2) | > 0 |
| categoria_sugerida_id | FK → categoria.id, nullable | research R6 |
| categoria_id | FK → categoria.id, nullable | the user's choice; starts equal to the suggestion |
| incluir | boolean | default true |
| movimentacao_id | FK → movimentacao.id, nullable, ON DELETE SET NULL | set on confirmation |

**Invariant on confirmation:** every item with `incluir = true` has `categoria_id` set, and that category has `tipo = SAIDA`.

### Movimentacao (changed)
- Add `fatura_id` (FK → fatura.id, nullable, ON DELETE SET NULL). This is the association `Fatura 0..1 → 0..* Movimentacao`. Movements stay valid if the invoice is removed (Sprint 4 §3.4).

## Non-persisted domain types (`backend/app/fatura/`)

| Type | Fields | Diagram |
|---|---|---|
| `DocumentoPDF` | `paginas: list[str]`, `palavras: list[Word]`, `texto: str` | input of `InterpretadorFatura` |
| `ItemExtraido` | `data: date`, `descricao: str`, `valor: Decimal` | elements of `List<Movimentacao>` in the diagram (draft form) |
| `InterpretadorFatura` (Protocol) | `nome`, `suporta(doc)`, `interpretar(doc)` | «interface» |
| `InterpretadorFaturaPDF` | the generic line-pattern implementation | realization |

**Δ:** in the diagram, `interpretar()` returns `List<Movimentacao>`. Here it returns `list[ItemExtraido]`, because the movements are created only after the user confirms (AD03). The intent is the same.

## Class diagram operations → code

| Diagram | Code |
|---|---|
| `Usuario.enviarFatura(arquivo): Fatura` | `fatura_service.enviar(db, usuario, upload)` |
| `Fatura.marcarInterpretada()` | `fatura.marcar_interpretada(interpretador, itens)` (model method) |
| `Fatura.marcarFalha(motivo)` | `fatura.marcar_falha(motivo)` (model method) |
| `InterpretadorFatura.suporta / interpretar` | `backend/app/fatura/interpretadores/*.py` |
