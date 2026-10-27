from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.enums import TipoMovimentacao
from app.models import Categoria


def listar(db: Session, tipo: TipoMovimentacao | None = None) -> Sequence[Categoria]:
    query = select(Categoria).order_by(Categoria.id)
    if tipo is not None:
        query = query.where(Categoria.tipo == tipo)
    return db.scalars(query).all()
