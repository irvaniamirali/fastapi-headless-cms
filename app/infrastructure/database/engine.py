from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.core.config import settings


def create_engine() -> AsyncEngine:
    return create_async_engine(
        str(settings.MAIN_DATABASE_CONNECTION_URL),
        echo=settings.ENABLE_SQL_STATEMENT_LOGGING,
        future=True,
    )
