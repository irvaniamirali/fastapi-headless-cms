import logging

from app.core.config import settings


def setup_logging():
    """
    Configure root logging for the whole app.
    """
    root_logger = logging.getLogger()
    if not root_logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(settings.LOGGING_FORMAT)
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)

    root_logger.setLevel(settings.LOGGING_LEVEL)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger by name (with app-wide settings).
    """
    return logging.getLogger(name)
