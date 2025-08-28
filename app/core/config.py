from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URI: str
    SQLALCHEMY_ECHO: bool = True

    JWT_SECRET_KEY: str
    JWT_ISSUER_SERVER: str

    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 15 * 60
    REFRESH_TOKEN_EXPIRE_SECONDS: int = 7 * 24 * 3600

    REDIS_URL: str = "redis://localhost:6379/0"

    ARGON2_TIME_COST: int = 2
    ARGON2_MEMORY_COST: int = 102400  # KB -> 100 MB
    ARGON2_PARALLELISM: int = 8

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()
