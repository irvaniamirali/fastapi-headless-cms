from fastapi import FastAPI

from app.api.v1.endpoints import router
from app.core.config import settings
from app.core.exceptions.app_exceptions import register_exception_handlers
from app.core.lifespan import lifespan
from app.core.logging import setup_logging
from app.middleware.registry import register_middlewares

setup_logging()  # initialize global logging


def create_application() -> FastAPI:
    """
    FastAPI application factory.

    Initializes the app with:
      - Lifespan context (startup/shutdown hooks)
      - Middlewares
      - API routers
      - Exception handlers
    """

    app = FastAPI(lifespan=lifespan, **settings.fastapi_kwargs)

    register_middlewares(app)
    app.include_router(router)
    register_exception_handlers(app)

    return app


app = create_application()
