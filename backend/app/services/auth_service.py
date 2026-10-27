from fastapi import status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.errors import DomainError
from app.core.security import hash_password, verify_password
from app.models import Usuario

# Verified when the email is unknown, so both login failures take the same time (US2-2).
_DUMMY_HASH = hash_password("upfinance-dummy-password")


def normalizar_email(email: str) -> str:
    return email.strip().lower()


def _email_ja_cadastrado() -> DomainError:
    return DomainError(
        "EMAIL_JA_CADASTRADO", "Este e-mail já está cadastrado", status.HTTP_409_CONFLICT
    )


def register(db: Session, nome: str, email: str, senha: str) -> Usuario:
    email = normalizar_email(email)
    if db.scalar(select(Usuario.id).where(Usuario.email == email)) is not None:
        raise _email_ja_cadastrado()

    usuario = Usuario(nome=nome.strip(), email=email, senha_hash=hash_password(senha))
    db.add(usuario)
    try:
        db.commit()
    except IntegrityError:  # concurrent registration with the same email
        db.rollback()
        raise _email_ja_cadastrado() from None
    return usuario


def authenticate(db: Session, email: str, senha: str) -> Usuario:
    usuario = db.scalar(select(Usuario).where(Usuario.email == normalizar_email(email)))
    senha_ok = verify_password(senha, usuario.senha_hash if usuario else _DUMMY_HASH)
    if usuario is None or not senha_ok:
        # Same message whether or not the email exists (US2-2)
        raise DomainError(
            "CREDENCIAIS_INVALIDAS", "E-mail ou senha inválidos.", status.HTTP_401_UNAUTHORIZED
        )
    return usuario
