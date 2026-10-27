from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


class DomainError(Exception):
    """Raised by services. Turned into the constitution's error shape (VIII)."""

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}


def error_response(
    status_code: int, code: str, message: str, details: dict[str, Any] | None = None
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"code": code, "message": message, "details": details or {}},
    )


_HTTP_CODES = {
    status.HTTP_401_UNAUTHORIZED: ("NAO_AUTENTICADO", "Faça login para continuar."),
    status.HTTP_404_NOT_FOUND: ("NAO_ENCONTRADO", "Recurso não encontrado."),
    status.HTTP_405_METHOD_NOT_ALLOWED: ("METODO_NAO_PERMITIDO", "Método não permitido."),
}


async def domain_error_handler(_: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, DomainError)
    return error_response(exc.status_code, exc.code, exc.message, exc.details)


async def validation_error_handler(_: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, RequestValidationError)
    campos: dict[str, str] = {}
    for err in exc.errors():
        loc = [str(part) for part in err["loc"] if part not in ("body", "query", "path")]
        campos[".".join(loc) or "_"] = err["msg"]
    return error_response(
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        "DADOS_INVALIDOS",
        "Dados inválidos.",
        {"campos": campos},
    )


async def http_error_handler(_: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, StarletteHTTPException)
    code, message = _HTTP_CODES.get(exc.status_code, ("ERRO_HTTP", str(exc.detail)))
    return error_response(exc.status_code, code, message)


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(DomainError, domain_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(StarletteHTTPException, http_error_handler)
