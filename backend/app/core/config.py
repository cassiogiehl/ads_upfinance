from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Read from environment variables only (Constitution IX)."""

    database_url: str
    # HS256 needs at least 32 bytes (RFC 7518 §3.2)
    jwt_secret: str = Field(min_length=32)
    jwt_ttl_hours: int = 8
    cors_origins: list[str] = ["http://localhost:5173"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
