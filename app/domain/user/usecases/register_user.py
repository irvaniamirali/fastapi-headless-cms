from app.common.exceptions.app_exceptions import (
    DuplicateEntryException,
    DatabaseOperationException,
)
from app.utils.auth.security import hash_password

from ..repositories import UserRepositoryInterface
from ..schemas import UserCreate, UserRead


class RegisterUser:

    def __init__(self, user_repository: UserRepositoryInterface) -> None:
        self.user_repository = user_repository

    async def execute(self, user_schema: UserCreate) -> UserRead:
        """
        Register a new user.

        Args:
            user_schema (UserCreate): User input data including email and password.

        Raises:
            DuplicateEntryException: If the email is already registered.
            DatabaseOperationException: If creating user fails.

        Returns:
            UserRead: The newly created user.
        """

        if await self.user_repository.exists("email", user_schema.email):
            raise DuplicateEntryException(field="email", value=str(user_schema.email))

        try:
            user = await self.user_repository.create_user(
                email=str(user_schema.email),
                password=hash_password(user_schema.password),
            )
        except Exception as e:
            raise DatabaseOperationException(
                operation="create",
                message=f"Failed to create user with email {user_schema.email}",
                data={"email": user_schema.email},
            ) from e

        return UserRead.model_validate(user)
