# Research: 002-analise-50-30-20

## R1: Analysis period (FR-010)

- **Status:** provisional default, pending clarification.
- **Decision:** `GET /analise?inicio=YYYY-MM-DD&fim=YYYY-MM-DD`, with both dates inclusive. Without parameters, the current calendar month in America/Sao_Paulo. The UI offers a month picker (previous and next month) plus a custom range.
- **Rationale:** income is usually monthly (the persona "recebe uma renda mensal"), so a monthly view is natural. A free range keeps the API general.

## R2: Alert deduplication

- **Decision:** at most one `AlertaLimite` per (usuario, pilar, periodo_inicio, periodo_fim), enforced by a partial unique index. Re-running the analysis behaves as follows:
  - pilar still exceeded with the same amount → no change
  - pilar still exceeded with a different amount → update `valor_excedido` and `mensagem`, set `lido = false`, refresh `data_emissao`
  - pilar no longer exceeded → keep the alert as history (no deletion)
- **Rationale:** the class diagram's multiplicity `AnaliseFinanceira 1 → 0..3 AlertaLimite` ("no máximo um alerta por pilar excedido"). Without deduplication, every page view would flood the alerts list.

## R3: Proactive trigger (US4)

- **Status:** provisional default, pending clarification.
- **Decision:** after `movimentacao_service.cadastrar` or `categorizar` succeeds for a movement in the **current month**, call `analise_service.avaliar_alertas(usuario, mes_corrente)`. It runs the same computation and upserts alerts (R2) inside the same transaction.
- **Rationale:** Sprint 2 US05 says "receber um alerta quando ultrapassar o limite". Reusing the same function keeps a single source for the rule. The cost is small (one aggregate query).
- **Alternative:** analysis-only trigger, which is the literal reading of UC06 «extend» UC05. Switching to it means removing one call.

## R4: Calculation (AD02 → algorithm)

```
def analisar(usuario, inicio, fim) -> AnaliseFinanceira | DadosInsuficientes:
    movs = movements of usuario with inicio <= data <= fim            # one query, aggregated in SQL
    renda = Σ valor where tipo = ENTRADA
    if no movs or renda == 0:                                         # AD02 guard / UC04 FA01
        return DadosInsuficientes
    totais = {p: Σ valor where tipo = SAIDA and categoria.pilar = p for p in Pilar}   # missing → 0
    distribuicoes = []
    for p in Pilar:                                                   # fork/join in AD02: independent per pilar
        limite = p.calcular_limite(renda)                             # RN003
        distribuicoes.append(DistribuicaoPilar(
            pilar=p, total_gasto=totais[p], limite=limite,
            percentual_utilizado=totais[p] / limite,                  # limite > 0 because renda > 0
            percentual_da_renda=totais[p] / renda,
            excedido=totais[p] > limite))                             # strictly greater (RN003)
    analise = AnaliseFinanceira(periodo, renda, distribuicoes, gerada_em=now())
    upsert AlertaLimite for each excedido (R2)                        # UC06 «extend»
    analise.interpretacao = interpretar(analise)                      # R5
    return analise
```

- Aggregation is a single `GROUP BY tipo, categoria.pilar` query.
- Arithmetic uses `Decimal`. Percentages are stored with 4 decimal places and shown with 2.

## R5: Interpretation templates (RF006, deterministic)

Messages are in pt-BR and are built in a fixed order: summary, then each pilar in the order ESSENCIAL, PESSOAL, FUTURO, then the conclusion.

| Key | Template |
|---|---|
| resumo | "No período de {inicio} a {fim}, sua renda foi de {renda} e seus gastos somaram {total_saidas} ({pct_renda_gasta} da renda). Saldo: {saldo}." |
| pilar_dentro | "{Pilar}: {total} de um limite de {limite} ({pct_utilizado} do limite de {pct_pilar}). Dentro do limite." |
| pilar_excedido | "{Pilar}: {total} de um limite de {limite}. Ultrapassou o limite em {excedente} ({pct_utilizado} do limite de {pct_pilar})." |
| conclusao_ok | "Sua distribuição está de acordo com a regra 50-30-20." |
| conclusao_excedido | "Atenção: {n} pilar(es) acima do limite: {lista}. Reveja os gastos desses pilares para equilibrar sua distribuição." |
| saldo_negativo | "Seus gastos superaram sua renda no período em {valor}." |

The API returns both `interpretacao` (the joined text) and `interpretacao_itens` (a list of `{chave, texto}`), so the UI can style each part.

## R6: Alert table design

- **Decision:** single-table inheritance for `Alerta`: one table `alerta` with discriminator `tipo` (`LIMITE` | `RECORRENCIA`) and nullable subtype columns. The `RECORRENCIA` columns are added by feature 004.
- **Rationale:** the alerts list is one query across both types. Few subtype columns.
