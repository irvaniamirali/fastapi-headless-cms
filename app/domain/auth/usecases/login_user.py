from app.core.exceptions.app_exceptions import InvalidCredentialsException, DatabaseOperationException
from app.domain.user.repositories import UserRepositoryInterface
from app.utils.security import verify_password
from app.utils.jwt import create_access_token

from ..schemas import Token


class LoginUser:
    """
    Use case for authenticating a user by email and password.

    Steps:
    1. Fetch the user from the repository by email.
    2. Raise DatabaseOperationException if a database error occurs.
    3. Validate the password; raise InvalidCredentialsException if invalid.
    4. Create and return a JWT access token wrapped in a Token schema.
    """

    def __init__(self, user_repository: UserRepositoryInterface) -> None:
        self.user_repository = user_repository

    async def execute(self, email: str, password: str) -> Token:
        try:
            user = await self.user_repository.get_by_email(email)
        except Exception as e:
            raise DatabaseOperationException(operation="select", message=str(e))

        if not user or not verify_password(password, user.password):
            raise InvalidCredentialsException()

        access_token = create_access_token(str(user.email))

        return Token(access_token=access_token)
