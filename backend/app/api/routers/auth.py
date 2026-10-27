from fastapi import APIRouter, status

from app.core.security import create_access_token
from app.deps import DbSession
from app.models import Usuario
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UsuarioOut
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


def _token_response(usuario: Usuario) -> TokenResponse:
    return TokenResponse(
        access_token=create_access_token(usuario.id),
        usuario=UsuarioOut.model_validate(usuario),
    )


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest, db: DbSession) -> TokenResponse:
    usuario = auth_service.register(db, body.nome, body.email, body.senha)
    return _token_response(usuario)


@router.post("/login")
def login(body: LoginRequest, db: DbSession) -> TokenResponse:
    usuario = auth_service.authenticate(db, body.email, body.senha)
    return _token_response(usuario)
