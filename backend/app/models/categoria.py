from sqlalchemy import CheckConstraint, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.domain.enums import Pilar, TipoMovimentacao


def varchar_enum(enum: type[Pilar] | type[TipoMovimentacao], name: str) -> Enum:
    """VARCHAR + CHECK instead of a native PG enum, portable to SQLite (research R4)."""
    return Enum(enum, native_enum=False, create_constraint=True, name=name)


class Categoria(Base):
    """System-provided catalog, seeded by migration 0001 (RN002, research R2)."""

    __tablename__ = "categoria"
    __table_args__ = (
        CheckConstraint(
            "(tipo = 'SAIDA' AND pilar IS NOT NULL) OR (tipo = 'ENTRADA' AND pilar IS NULL)",
            name="ck_categoria_pilar_por_tipo",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(80), unique=True)
    tipo: Mapped[TipoMovimentacao] = mapped_column(varchar_enum(TipoMovimentacao, "ck_tipo"))
    pilar: Mapped[Pilar | None] = mapped_column(varchar_enum(Pilar, "ck_pilar"))
