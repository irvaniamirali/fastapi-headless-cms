from app.core.exceptions.app_exceptions import (
    ConflictException,
    DatabaseOperationException,
)
from app.utils.security import hash_password

from ..repositories import UserRepositoryInterface
from ..schemas import UserCreate, UserRead
from ..models import User


class RegisterUser:
    """
    Use case for registering a new user.

    Steps:
    1. Check if the email is already registered; raise ConflictException if it exists.
    2. Hash the user's password.
    3. Insert the new user into the repository; raise DatabaseOperationException on failure.
    4. Return the created user as a UserRead schema.
    """

    def __init__(self, user_repository: UserRepositoryInterface) -> None:
        self.user_repository = user_repository

    async def execute(self, user_schema: UserCreate):
        if await self.user_repository.exists("email", user_schema.email):
            raise ConflictException("Email already registered.")

        user = User(
            email=user_schema.email, password=hash_password(user_schema.password)
        )

        try:
            await self.user_repository.insert(user)
        except Exception as e:
            raise DatabaseOperationException(operation="insert") from e

        return UserRead.model_validate(user)
