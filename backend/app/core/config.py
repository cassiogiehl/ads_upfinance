from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Read from environment variables only (Constitution IX)."""

    database_url: str
    jwt_secret: str
    jwt_ttl_hours: int = 8
    cors_origins: list[str] = ["http://localhost:5173"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
