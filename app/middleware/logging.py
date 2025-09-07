import time

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.core.logging import get_logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, log_format: str = settings.REQUEST_LOG_FORMAT):
        super().__init__(app)
        self.logger = get_logger("app.request")
        self.log_format = log_format

    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        elapsed = time.perf_counter() - start

        self.logger.info(
            f"{request.method} {request.url.path} -> {response.status_code} ({elapsed:.4f}s)"
        )
        return response


def add_request_logging(app: FastAPI, log_format: str = settings.REQUEST_LOG_FORMAT):
    app.add_middleware(RequestLoggingMiddleware, log_format=log_format)  # type: ignore
