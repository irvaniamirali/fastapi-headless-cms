from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.domain.auth.schemas import Token
from app.domain.user.schemas import UserRead
from app.domain.user.repositories import UserRepositoryInterface
from app.domain.user.depends import get_user_repository

from .depends import get_current_authenticated_user
from .usecases.login_user import LoginUser

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post(
    "/login",
    response_model=Token,
    summary="Authenticate user and return access token",
    responses={
        200: {"description": "Successful login, returns access token"},
        401: {"description": "Invalid credentials"},
        404: {"description": "User not found"},
        500: {"description": "Internal server error"}
    }
)
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
):
    """
    Login endpoint for users.

    - **username**: email of the user
    - **password**: raw password
    - **returns**: access token (JWT)
    """

    email = form_data.username
    password = form_data.password

    return await LoginUser(user_repository).execute(email, password)


@router.get(
    "/me",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Get current authenticated user",
)
async def get_current_user(current_user: Annotated[UserRead, Depends(get_current_authenticated_user)]):
    """
    Return the information of the currently authenticated user.

    - **Requires**: Bearer access token
    - **Returns**: User details (`id`, `email`, `is_active`, `created_at`, ...)
    - **Raises**: 401 Unauthorized if the token is missing or invalid
    """
    return current_user
