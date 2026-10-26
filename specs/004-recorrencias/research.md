# Research: 004-recorrencias

## R1: Detection algorithm (AD04 → code)

`IdentificadorRecorrencia` («service» in Sprint 4) is a pure function over a list of movements:

```
def identificar(historico: list[Movimentacao], hoje: date) -> list[Candidato]:
    saidas = [m for m in historico if m.tipo == SAIDA and m.data >= hoje - 365 days]
    grupos = group_by(saidas, key=normalizar_descricao(m.descricao))       # AD04 "Agrupar por descrição semelhante"
    candidatos = []
    for chave, movs in grupos:                                             # AD04 "Analisar grupo *"
        movs = sorted(movs, key=data)
        movs = dedupe_same_day(movs)                                       # 2 charges on the same day count as one occurrence
        if len(movs) < 2: continue                                         # multiplicity 2..*
        intervalos = [b.data - a.data for a, b in pairwise(movs)]
        freq = classificar(intervalos)                                     # R2
        if freq is None: continue                                          # UC09 FA01
        if not valores_semelhantes([m.valor for m in movs]): continue      # R2
        candidatos.append(Candidato(chave, movs, freq,
                                    valor_medio=mean(valores),
                                    proximo=projetar(movs[-1].data, freq)))   # R3
    return candidatos
```

- `normalizar_descricao` is shared with 003 (`backend/app/fatura/normalizacao.py`). It uppercases, strips accents, removes digits, `*`, punctuation and the installment markers `PARC nn/nn`, collapses whitespace, and drops the noise tokens `CONTA`, `PGTO`, `PAGAMENTO`, `DEB AUT`. If 004 is built before 003, the task creates this module.
- The function is pure, so it is unit-tested without a database.

## R2: Frequencies and tolerances (FR-003)

- **Status:** provisional defaults, pending clarification.

| Frequência | Nominal days | Each interval must fall in | `periodicidade_dias` |
|---|---|---|---|
| SEMANAL | 7 | 5–9 | 7 |
| MENSAL | 30 | 25–35 | 30 |
| ANUAL | 365 | 350–380 | 365 |

- **Every** interval must fall in the same band. The first band that fits all intervals wins.
- **Similar amounts:** `max(|v − mediana|) / mediana ≤ 0.30`. This allows the variation of utility bills (água and luz) while rejecting unrelated purchases at the same merchant.
- **Rationale:** the glossary examples (água, luz, internet) are monthly with variable amounts. A 30% band covers seasonal swings in electricity bills.

## R3: Projecting the next due date

- MENSAL: same day of the month as the last occurrence, next month. Clamped to the month's last day (`dateutil.relativedelta(months=+1)`). If that date is already in the past, keep advancing until it is ≥ today.
- SEMANAL and ANUAL: `ultima + periodicidade_dias`, advanced the same way.
- **Inactive:** `hoje − ultima_ocorrencia > 2 × periodicidade_dias`. No reminders. Listed under "Inativos". It reactivates automatically when a new occurrence appears.

## R4: Alerts (FR-006, FR-007)

| Motivo | When | Message (pt-BR) | Dedup key |
|---|---|---|---|
| `IDENTIFICADA` | a recurrence is created for the first time | "Identificamos um pagamento recorrente: {descricao}, cerca de {valor_medio} {freq_label}. Próximo vencimento previsto: {data}." | (recorrência, motivo) |
| `VENCIMENTO_PROXIMO` | `0 ≤ proximo_vencimento − hoje ≤ 3` days, active, not dismissed, and no occurrence yet in the current cycle | "{descricao} vence em {n} dia(s) ({data}), valor estimado {valor_medio}." | (recorrência, motivo, proximo_vencimento) |

- **Reminder trigger, with no scheduler (Constitution VI):** reminders are evaluated lazily by `recorrencia_service.gerar_lembretes(usuario, hoje)`, which runs at the start of `GET /alertas` and `GET /recorrencias`. The user sees reminders whenever they open the app. A background scheduler can replace this later without changing the contract.
- **Reminder window:** 3 days is a provisional default, pending clarification.

## R5: Dismissal (FR-009)

- **Status:** provisional, pending clarification.
- `PATCH /recorrencias/{id}` with `{"descartado": true}`. A dismissed recurrence keeps its row, so identification won't recreate it (same `descricao_normalizada`), and it never alerts. Unread alerts for it are marked as read.

## R6: Reference dataset for SC-001

`backend/tests/fixtures/historico_recorrencias.py` builds a 12-month synthetic history containing:
- true recurrences: water, electricity, internet, streaming, gym, rent (monthly); annual insurance
- noise: iFood several times a month at irregular intervals, supermarket trips, a one-off appliance purchase, and two Uber rides 30 days apart with very different amounts

The expected recurrences are listed alongside, and a test computes precision and recall.

## R7: Persisting the link to movements

- **Decision:** a nullable FK `movimentacao.pagamento_recorrente_id`. This follows the diagram's `PagamentoRecorrente 0..1 → 2..* Movimentacao`: a movement belongs to at most one recurrence.
- **Rationale:** simpler than a link table (Constitution VI), and the 0..1 multiplicity makes a join table unnecessary. This replaces the link table mentioned in the initial plan.
- On each run, the FKs of the group's movements are set and stale links are cleared.

## R8: When identification runs (FR-005)

- Synchronously, at the end of `movimentacao_service.cadastrar` and `categorizar` (SAIDA only), `fatura_service.confirmar`, and `POST /recorrencias/identificar`.
- The cost is one query (≤ 12 months of SAIDA for one user), then grouping in memory. It must stay under 1 s for 2,000 movements (SC-002).
