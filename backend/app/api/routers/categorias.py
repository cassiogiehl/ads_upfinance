from fastapi import APIRouter

from app.deps import CurrentUser, DbSession
from app.domain.enums import TipoMovimentacao
from app.schemas.categoria import CategoriaOut
from app.services import categoria_service

router = APIRouter(prefix="/categorias", tags=["categorias"])


@router.get("")
def listar(
    _: CurrentUser, db: DbSession, tipo: TipoMovimentacao | None = None
) -> list[CategoriaOut]:
    return [CategoriaOut.model_validate(c) for c in categoria_service.listar(db, tipo)]
