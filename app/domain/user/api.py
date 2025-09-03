from typing import Annotated

from fastapi import APIRouter, Depends, status

from .depends import get_user_repository
from .repositories import UserRepositoryInterface
from .schemas import UserCreate, UserRead
from .usecases.register_user import RegisterUser

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    responses={
        201: {"description": "User successfully created"},
        409: {"description": "Email already registered"},
        500: {"description": "Internal server error"},
    },
)
async def register_user(
        user_schema: UserCreate,
        user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)]
):
    """
    Endpoint to register a new user.

    - **user_schema**: UserCreate schema with `email` and `password`.
    - **returns**: UserRead schema of the newly created user.
    - **raises**: ConflictException if email already exists, DatabaseOperationException on DB error.
    """
    return await RegisterUser(user_repository).execute(user_schema)
