from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    OPENAI_API_KEY: str | None = None
    ANTHROPIC_API_KEY: str | None = None
    REDIS_URL: str = "redis://redis:6379/0"


    class Config:
        env_file = ".env"


settings = Settings()