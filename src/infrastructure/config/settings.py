# src/infrastructure/config/settings.py
import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "LogitrackAPI"

    DATABASE_URL: str = ""
    REDIS_URL: str = ""

    EXTERNAL_API_KEY: str | None = None
    EXTERNAL_API_HOST: str | None = None
    EXTERNAL_API_BASE_URL: str | None = None
    JWT_SECRET_KEY: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @property
    def is_test_mode(self) -> bool:
        """Verifica se está rodando em modo de teste (pytest)"""
        return os.getenv("PYTEST_CURRENT_TEST", "") != ""


settings = Settings()


if not settings.is_test_mode:
    if not settings.DATABASE_URL:
        raise ValueError("DATABASE_URL não encontrado no .env")
    if not settings.REDIS_URL:
        raise ValueError("REDIS_URL não encontrado no .env")
else:
    if not settings.DATABASE_URL:
        settings.DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/logitrack_test"
    if not settings.REDIS_URL:
        settings.REDIS_URL = "redis://localhost:6379/0"
    if not settings.JWT_SECRET_KEY:
        settings.JWT_SECRET_KEY = "test-secret-key-for-unit-tests"


if not settings.is_test_mode:
    if settings.EXTERNAL_API_KEY is None:
        print("⚠️  Aviso: EXTERNAL_API_KEY não configurada → endpoints externos podem falhar")
