from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

from app.core.config import get_settings

ALGORITHM = "HS256"

_password_hash = PasswordHash((Argon2Hasher(),))


def hash_password(senha: str) -> str:
    return _password_hash.hash(senha)


def verify_password(senha: str, senha_hash: str) -> bool:
    return _password_hash.verify(senha, senha_hash)


def create_access_token(usuario_id: int) -> str:
    settings = get_settings()
    agora = datetime.now(UTC)
    payload = {
        "sub": str(usuario_id),
        "iat": agora,
        "exp": agora + timedelta(hours=settings.jwt_ttl_hours),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGORITHM)


def decode_access_token(token: str) -> int | None:
    """Returns the user id, or None when the token is invalid or expired."""
    try:
        payload = jwt.decode(
            token,
            get_settings().jwt_secret,
            algorithms=[ALGORITHM],
            options={"require": ["sub", "exp"]},
        )
        return int(payload["sub"])
    except (jwt.InvalidTokenError, ValueError):
        return None
