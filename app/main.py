from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.endpoints import router
from app.infrastructure.database.base import Base
from app.infrastructure.database.session import engine
from app.core.exceptions import AppBaseException, app_exception_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- startup ---
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # --- shutdown ---
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(router)

app.add_exception_handler(AppBaseException, app_exception_handler)
