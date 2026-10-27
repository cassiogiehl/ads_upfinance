"""T013 · Pilar enum (RN001, RN003, RN004; Sprint 4 §3.5)."""

from decimal import Decimal

import pytest

from app.domain.enums import Pilar, TipoMovimentacao


@pytest.mark.parametrize(
    ("pilar", "esperado"),
    [
        (Pilar.ESSENCIAL, Decimal("5000.00")),
        (Pilar.PESSOAL, Decimal("3000.00")),
        (Pilar.FUTURO, Decimal("2000.00")),
    ],
)
def test_calcular_limite_rn003_example(pilar: Pilar, esperado: Decimal) -> None:
    limite = pilar.calcular_limite(Decimal("10000"))

    assert isinstance(limite, Decimal)
    assert limite == esperado


def test_percentuais_are_fixed_decimals_that_sum_to_one() -> None:
    assert [p.percentual for p in Pilar] == [Decimal("0.50"), Decimal("0.30"), Decimal("0.20")]
    assert all(isinstance(p.percentual, Decimal) for p in Pilar)
    assert sum(p.percentual for p in Pilar) == Decimal("1.00")


def test_labels_are_pt_br() -> None:
    assert [p.label for p in Pilar] == ["Essencial", "Pessoal", "Futuro"]


def test_enums_serialize_as_their_names() -> None:
    assert Pilar.ESSENCIAL == "ESSENCIAL"
    assert [t.value for t in TipoMovimentacao] == ["ENTRADA", "SAIDA"]
