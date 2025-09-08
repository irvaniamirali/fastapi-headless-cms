from enum import StrEnum


class ErrorCode(StrEnum):
    """
    Enumeration of application-wide error codes.

    This class defines standardized string-based error codes used across
    the application for consistent error handling, logging, and API responses.

    Each error code corresponds to a specific category of error:
    - DATABASE_ERROR: Errors related to database operations or connections.
    - CONFLICT: Resource conflicts, e.g., when a unique constraint is violated.
    - UNAUTHORIZED: Authentication failure (invalid or missing credentials).
    """

    CONFLICT = "CONFLICT"
    DATABASE_ERROR = "DATABASE_ERROR"
    UNAUTHORIZED = "UNAUTHORIZED"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    NOT_FOUND = "NOT_FOUND"
