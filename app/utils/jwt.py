from datetime import datetime, timedelta, timezone

from jose import jwt

from app.core.config import settings


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    expiration_time = datetime.now(timezone.utc) + (
        expires_delta or settings.jwt_access_token_expiration
    )
    payload = {"sub": subject, "exp": expiration_time}
    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY.get_secret_value(),
        algorithm=settings.JWT_SIGNING_ALGORITHM,
    )
