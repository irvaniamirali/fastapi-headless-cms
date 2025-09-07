from fastapi import FastAPI

from app.core.config import settings

from .cors import add_cors_middleware
from .gzip import add_gzip_middleware
from .logging import add_request_logging


def register_middlewares(app: FastAPI) -> None:
    """Register all middlewares in the application, based on settings."""

    add_cors_middleware(
        app,
        settings.CORS_ALLOWED_ORIGINS,
        expose_headers=["X-Correlation-ID"],
    )

    add_gzip_middleware(app)

    add_request_logging(app, settings.REQUEST_LOG_FORMAT)
