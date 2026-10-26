# Data Model: 002-analise-50-30-20

Source: the Sprint 4 class diagram (`AnaliseFinanceira`, `DistribuicaoPilar`, `Alerta`, `AlertaLimite`).

## Computed (not persisted)

### AnaliseFinanceira
| Field | Type | Diagram |
|---|---|---|
| periodo_inicio, periodo_fim | date | `periodo` |
| renda | Decimal | `/renda` (derived: Σ ENTRADA) |
| total_saidas | Decimal | |
| saldo | Decimal | renda − total_saidas |
| distribuicoes | list[DistribuicaoPilar], exactly 3 | composition 1 — 3 |
| interpretacao | str | `getInterpretacao()` |
| interpretacao_itens | list[{chave, texto}] | |
| pilares_excedidos | list[Pilar] | `getPilaresExcedidos()` |
| alertas_gerados | list[AlertaLimite] | association 1 — 0..3 |
| gerada_em | datetime | `dataGeracao` |

The operation `calcularDistribuicao()` is implemented as `analise_service.analisar(...)` (research R4).

### DistribuicaoPilar
| Field | Type | Diagram |
|---|---|---|
| pilar | Pilar | `pilar` |
| total_gasto | Decimal | `totalGasto` |
| limite | Decimal | `limite` |
| percentual_utilizado | Decimal (total/limite) | `getPercentualUtilizado()` |
| percentual_da_renda | Decimal (total/renda) | |
| excedido | bool | `isExcedido()` |
| excedente | Decimal (max(0, total − limite)) | |

Both are frozen dataclasses in `backend/app/domain/analise.py`. They are pure, with no database access, which makes them easy to unit-test.

### DadosInsuficientes
`{situacao: "DADOS_INSUFICIENTES", mensagem}` is returned instead of an analysis (UC04 FA01).

## Persisted

### Alerta (`alerta`): single-table inheritance (research R6)

| Field | Type | Rules | Diagram |
|---|---|---|---|
| id | integer PK | | `id` |
| usuario_id | FK → usuario.id ON DELETE CASCADE | indexed | Usuario 1 — 0..* Alerta |
| tipo | varchar(11) | `LIMITE` or `RECORRENCIA` (CHECK) | generalization discriminator |
| mensagem | varchar(500) | required | `mensagem` |
| data_emissao | timestamp UTC | required | `dataEmissao` |
| lido | boolean | default false | `lido` |
| **AlertaLimite columns** | | | |
| pilar | varchar(9), nullable | required when tipo = LIMITE | `AlertaLimite.pilar` |
| valor_excedido | NUMERIC(12,2), nullable | > 0 when tipo = LIMITE | `AlertaLimite.valorExcedido` |
| periodo_inicio, periodo_fim | date, nullable | required when tipo = LIMITE | (needed for deduplication, research R2) |
| **AlertaRecorrencia columns** | | added in feature 004 | |

**Constraints**
- CHECK: `tipo <> 'LIMITE' OR (pilar IS NOT NULL AND valor_excedido IS NOT NULL AND periodo_inicio IS NOT NULL AND periodo_fim IS NOT NULL)`
- Partial unique index `ux_alerta_limite_periodo` on `(usuario_id, pilar, periodo_inicio, periodo_fim) WHERE tipo = 'LIMITE'` (research R2)
- Index `(usuario_id, lido, data_emissao DESC)`

**ORM:** `Alerta` is the base with `__mapper_args__ = {"polymorphic_on": tipo}`. `AlertaLimite(Alerta)` has `polymorphic_identity="LIMITE"`.

**Operation:** `Alerta.marcarComoLido()` maps to `alerta_service.marcar_lido(db, usuario, alerta_id)`.
