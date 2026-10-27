from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, ConfigDict, EmailStr, Field, StringConstraints


def _strip(value: object) -> object:
    return value.strip() if isinstance(value, str) else value


Nome = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=120)]
Email = Annotated[EmailStr, BeforeValidator(_strip), Field(max_length=254)]


class RegisterRequest(BaseModel):
    nome: Nome
    email: Email
    senha: Annotated[str, Field(min_length=8, max_length=128)]  # FR-008


class LoginRequest(BaseModel):
    # Not validated as an email: a malformed one is just wrong credentials (US2-2)
    email: str
    senha: str


class UsuarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    usuario: UsuarioOut
