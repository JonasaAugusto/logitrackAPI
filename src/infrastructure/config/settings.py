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


settings = Settings()


if not settings.DATABASE_URL:
    raise ValueError("DATABASE_URL não encontrado no .env")
if not settings.REDIS_URL:
    raise ValueError("REDIS_URL não encontrado no .env")

if settings.EXTERNAL_API_KEY is None:
    print("Aviso: EXTERNAL_API_KEY não configurada → endpoints externos podem falhar")
