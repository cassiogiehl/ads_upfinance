from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.errors import DomainError
from app.core.security import decode_access_token
from app.db import SessionLocal
from app.models import Usuario

_bearer = HTTPBearer(auto_error=False)


def get_db() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session


DbSession = Annotated[Session, Depends(get_db)]


def get_current_user(
    db: DbSession,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
) -> Usuario:
    usuario_id = decode_access_token(credentials.credentials) if credentials else None
    usuario = db.get(Usuario, usuario_id) if usuario_id is not None else None
    if usuario is None:
        raise DomainError(
            "NAO_AUTENTICADO", "Faça login para continuar.", status.HTTP_401_UNAUTHORIZED
        )
    return usuario


CurrentUser = Annotated[Usuario, Depends(get_current_user)]
