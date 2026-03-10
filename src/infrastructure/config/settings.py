import os
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "LogitrackAPI"

    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/logitrack"
    REDIS_URL: str = "redis://localhost:6379/0"

    EXTERNAL_API_KEY: Optional[str] = None
    EXTERNAL_API_HOST: Optional[str] = None
    EXTERNAL_API_BASE_URL: Optional[str] = None
    JWT_SECRET_KEY: str = "test-secret-key-for-unit-tests"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @property
    def is_test_mode(self) -> bool:
        return "PYTEST_CURRENT_TEST" in os.environ


settings = Settings()

if not settings.is_test_mode:
    if not settings.DATABASE_URL:
        raise ValueError("DATABASE_URL não configurado!")
    if not settings.REDIS_URL:
        raise ValueError("REDIS_URL não configurado!")
    if not settings.EXTERNAL_API_KEY:
        print("⚠️  Aviso: EXTERNAL_API_KEY não configurada.")
