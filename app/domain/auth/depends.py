from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.config import settings
from app.domain.user.repositories import UserRepositoryInterface
from app.domain.user.depends import get_user_repository
from app.domain.user.models import User

from .schemas import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_authenticated_user(
    user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
    access_token: str = Depends(oauth2_scheme),
) -> User:
    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        decoded_payload = jwt.decode(
            access_token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        token_payload = TokenPayload(**decoded_payload)
    except (JWTError, ValueError):
        raise unauthorized_exception

    if not token_payload.sub:
        raise unauthorized_exception

    user_entity = await user_repository.get_by_email(token_payload.sub)
    if not user_entity:
        raise unauthorized_exception

    return user_entity
