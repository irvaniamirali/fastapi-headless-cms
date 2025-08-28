from sqlalchemy.ext.asyncio import AsyncEngine

from .session import engine
from .base import Base


async def initialize_database(_engine: AsyncEngine = engine):

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
