from fastapi import FastAPI, status
from contextlib import asynccontextmanager

from app.api.v1.endpoints import router
from app.core.exception_handlers import register_exception_handlers
from app.infrastructure.database import initialize_database

@asynccontextmanager
async def lifespan(_app: FastAPI):
    await initialize_database()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(router)

register_exception_handlers(app)

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Server is up and running"}
