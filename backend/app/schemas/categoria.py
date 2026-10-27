from pydantic import BaseModel, ConfigDict

from app.domain.enums import Pilar, TipoMovimentacao


class CategoriaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    tipo: TipoMovimentacao
    pilar: Pilar | None


class PilarInfo(BaseModel):
    pilar: Pilar
    percentual: str  # Decimal as a string, e.g. "0.50" (Constitution IV)
    label: str
