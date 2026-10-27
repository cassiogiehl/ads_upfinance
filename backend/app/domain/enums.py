from decimal import Decimal
from enum import StrEnum


class TipoMovimentacao(StrEnum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"


class Pilar(StrEnum):
    """The fixed 50-30-20 pilares (RN001, RN004). Mirrors Sprint 4 §3.5."""

    ESSENCIAL = "ESSENCIAL"
    PESSOAL = "PESSOAL"
    FUTURO = "FUTURO"

    @property
    def percentual(self) -> Decimal:
        return _PERCENTUAIS[self]

    @property
    def label(self) -> str:
        return _LABELS[self]

    def calcular_limite(self, renda: Decimal) -> Decimal:
        """Spending ceiling for this pilar (RN003)."""
        return renda * self.percentual


_PERCENTUAIS = {
    Pilar.ESSENCIAL: Decimal("0.50"),
    Pilar.PESSOAL: Decimal("0.30"),
    Pilar.FUTURO: Decimal("0.20"),
}

_LABELS = {
    Pilar.ESSENCIAL: "Essencial",
    Pilar.PESSOAL: "Pessoal",
    Pilar.FUTURO: "Futuro",
}
