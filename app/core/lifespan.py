from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infrastructure.database.base import Base
from app.infrastructure.database.engine import create_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage DB engine lifecycle:
    - On startup: create engine & tables, attach to app.state.
    - On shutdown: dispose engine.
    """
    engine = create_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    app.state.db_engine = engine
    yield
    await app.state.db_engine.dispose()
