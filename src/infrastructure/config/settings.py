from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore")

    PROJECT_NAME: str = "LogitrackAPI"
    DATABASE_URL: str = Field(default="")
    REDIS_URL: str | None = None


settings = Settings()
