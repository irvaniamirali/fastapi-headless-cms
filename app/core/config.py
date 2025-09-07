import logging
from datetime import timedelta
from functools import lru_cache
from typing import Any

from pydantic import PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings class, handling configuration from environment variables
    and .env files.
    """

    APPLICATION_NAME: str = "FastAPI Headless CMS"
    APPLICATION_VERSION: str = "1.0.0"
    ENABLE_SQL_STATEMENT_LOGGING: bool = False
    ENABLE_DEBUG_MODE: bool = False

    API_ROUTE_PREFIX: str = "/api"
    DOCUMENTATION_URL_PATH: str = "/docs"
    OPENAPI_SCHEMA_PREFIX: str = ""
    OPENAPI_SCHEMA_URL_PATH: str = "/openapi.json"
    REDOC_DOCUMENTATION_URL_PATH: str = "/redoc"

    TEST_DATABASE_CONNECTION_URL: str
    MAIN_DATABASE_CONNECTION_URL: PostgresDsn | str
    ENABLE_SQL_ECHO_LOGGING: bool = False

    JWT_SECRET_KEY: SecretStr
    JWT_SIGNING_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    CORS_ALLOWED_ORIGINS: list[str] = ["*"]
    ALLOWED_HOSTNAMES: list[str] = ["*"]

    LOGGING_LEVEL: int = logging.INFO
    LOGGING_FORMAT: str = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    REQUEST_LOG_FORMAT: str = "%(method)s %(url)s -> %(status)d (%(time).4fs)"

    @property
    def jwt_access_token_expiration(self) -> timedelta:
        return timedelta(minutes=self.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        return {
            "title": self.APPLICATION_NAME,
            "version": self.APPLICATION_VERSION,
            "debug": self.ENABLE_DEBUG_MODE,
            "docs_url": self.DOCUMENTATION_URL_PATH,
            "openapi_prefix": self.OPENAPI_SCHEMA_PREFIX,
            "openapi_url": self.OPENAPI_SCHEMA_URL_PATH,
            "redoc_url": self.REDOC_DOCUMENTATION_URL_PATH,
        }

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        validate_assignment=True,
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached instance of the Settings class.
    This ensures the settings are loaded only once.
    """
    return Settings()  # type: ignore[call-arg]


settings = get_settings()
