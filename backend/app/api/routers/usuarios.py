from fastapi import APIRouter

from app.deps import CurrentUser
from app.schemas.auth import UsuarioOut

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("/me")
def me(usuario: CurrentUser) -> UsuarioOut:
    return UsuarioOut.model_validate(usuario)
