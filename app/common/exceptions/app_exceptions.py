import datetime

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.common.http_responses.error_response import ErrorCodes, ErrorResponse


class AppBaseException(Exception):
    def __init__(
        self,
        *,
        code: ErrorCodes,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        data: dict | None = None
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.data = data or {}

    def to_response_model(self, path: str = "") -> ErrorResponse:
        return ErrorResponse(
            code=self.code,
            message=self.message,
            status=self.status_code,
            timestamp=datetime.datetime.now(datetime.timezone.utc),  # RFC 3339-compliant
            path=path,
            data=self.data,
        )


class DatabaseOperationException(AppBaseException):
    def __init__(
        self,
        operation: str | None = None,
        message: str | None = None,
        data: dict | None = None
    ):
        message = f"Failed to perform {operation} operation. {message} "

        super().__init__(
            code=ErrorCodes.DATABASE_ERROR,
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data=data,
        )


class InvalidTokenException(AppBaseException):
    """Raised when ."""

    def __init__(self, message="Invalid token", token: str = "No token provided"):
        super().__init__(
            code=ErrorCodes.INVALID_TOKEN,
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            data={"token": token}
        )


class DuplicateEntryException(AppBaseException):
    def __init__(self, field: str, value: str):
        super().__init__(
            code=ErrorCodes.DUPLICATE_ENTRY,
            message=f"{field} '{value}' already exists.",
            status_code=status.HTTP_409_CONFLICT,
            data={field: value},
        )


class EntityNotFoundException(AppBaseException):
    def __init__(self, data: dict, message: str = "Entity not found"):
        super().__init__(
            code=ErrorCodes.ENTITY_NOT_FOUND,
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            data=data,
        )


class InvalidCredentialsException(AppBaseException):
    def __init__(self, data=None, message: str = "Authentication failed"):
        super().__init__(
            code=ErrorCodes.INVALID_CREDENTIALS,
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            data=data or {}
        )


class PermissionDeniedException(AppBaseException):
    def __init__(self, message: str = "Permission denied", data: dict | None = None):
        super().__init__(
            code=ErrorCodes.PERMISSION_DENIED,
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            data=data or {},
        )


class ValidationException(AppBaseException):
    def __init__(self, message: str = "Validation failed", data: dict | None = None):
        super().__init__(
            code=ErrorCodes.VALIDATION_ERROR,
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            data=data or {},
        )

async def handle_app_exception(request: Request, exc: AppBaseException):
    error_model = exc.to_response_model(path=request.url.path)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": error_model.model_dump(mode="json")},
    )


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(AppBaseException, handle_app_exception)
