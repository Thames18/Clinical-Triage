from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""

    REDIS_URL: str = "redis://redis:6379/0"
    NEXT_PUBLIC_API_URL: str = "http://localhost:8000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    JWT_SECRET_KEY: str = "change-this-in-production"
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD_HASH: str = ""

settings = Settings()