from datetime import timedelta

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Headless CMS"
    DEBUG: bool = False

    JWT_SECRET_KEY: str = "change-this-in-prod-super-secret-key"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_ALGORITHM: str = "HS256"

    DATABASE_URL: str = "sqlite+aiosqlite:///database.db"
    TEST_DATABASE_URL: str = "sqlite+aiosqlite:///test-database.db"

    @property
    def access_token_expires(self) -> timedelta:
        return timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
