from typing import Any

from fastapi import Request, status
from fastapi.responses import JSONResponse

from .error_codes import ErrorCode


class AppBaseException(Exception):
    """Base class for all custom exceptions in the application."""

    def __init__(
        self,
        *,
        message: str,
        status_code: int,
        error_code: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> dict[str, Any]:
        """Convert exception details to dict for JSON response."""
        return {
            "error": {
                "message": self.message,
                "code": self.error_code,
                "status": self.status_code,
                "details": self.details,
            }
        }


class ConflictException(AppBaseException):
    def __init__(
        self,
        message: str = "Conflict",
        error_code: str = ErrorCode.CONFLICT,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            error_code=error_code,
            details=details,
        )


class DatabaseOperationException(AppBaseException):
    def __init__(
        self,
        operation: str,
        message: str = "Database operation failed",
        error_code: str = ErrorCode.DATABASE_ERROR,
        internal_error: str | None = None,
    ) -> None:
        details = {"operation": operation}
        if internal_error:
            details["internal_error"] = internal_error

        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code=error_code,
            details=details,
        )


class InvalidCredentialsException(AppBaseException):
    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code=ErrorCode.UNAUTHORIZED,
        )


class PermissionDeniedException(AppBaseException):
    def __init__(self, message: str = "Permission denied"):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code=ErrorCode.PERMISSION_DENIED,
        )


class ValidationException(AppBaseException):
    def __init__(
        self,
        message: str = "Validation error",
        error_code: str = "VALIDATION_ERROR",
        details: dict[str, Any] | None = None,
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code=error_code,
            details=details,
        )


class NotFoundException(AppBaseException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ErrorCode.NOT_FOUND,
        )


async def app_exception_handler(request: Request, exc: AppBaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
    )
