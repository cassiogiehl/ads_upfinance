from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import auth, categorias, pilares, usuarios
from app.core.config import get_settings
from app.core.errors import register_exception_handlers

API_PREFIX = "/api/v1"


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="UPFinance API", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_exception_handlers(app)

    api = APIRouter(prefix=API_PREFIX)
    for router in (auth.router, usuarios.router, categorias.router, pilares.router):
        api.include_router(router)
    app.include_router(api)
    return app


app = create_app()
