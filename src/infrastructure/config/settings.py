from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore")

    PROJECT_NAME: str = "LogitrackAPI"

    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/logitrack"

    REDIS_URL: str = "redis://localhost:6379/0"


settings = Settings()
