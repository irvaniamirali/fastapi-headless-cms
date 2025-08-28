from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer

from app.common.exceptions.app_exceptions import EntityNotFoundException
from app.domain.auth.schemas import JWTPayload
from app.domain.auth.usecases.read_jwt_token import ReadJwtToken
from app.domain.user.depends import get_user_repository
from app.domain.user.repositories.interface import UserRepositoryInterface
from app.domain.user.schemas import UserRead

oauth2_bearer = OAuth2PasswordBearer(
    tokenUrl="/auth/token/swagger",
)


async def get_current_authenticated_user(
        token: str = Depends(oauth2_bearer),
        user_repository: UserRepositoryInterface = Depends(get_user_repository),
) -> UserRead:
    """
    Get the current authenticated user based on the provided token.

    Args:
        token (str): The access token.
        user_repository (UserRepositoryInterface): The user repository.

    Returns:
        UserRead: The authenticated user.
    """
    payload: JWTPayload = await ReadJwtToken(token).execute()
    user_id = payload.sub
    user = await user_repository.get_by_id(user_id)
    if not user:
        raise EntityNotFoundException(data={"user_id": user_id}, message="User not found")
    return UserRead.model_validate(user)
