from typing import Annotated

from fastapi import APIRouter, Request, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.common.http_responses import SuccessResponse
from app.common.http_responses.success_result import SuccessResult, SuccessCodes
from app.domain.auth.schemas import Token
from app.domain.user.depends import get_user_repository
from app.domain.user.repositories import UserRepositoryInterface
from app.domain.user.schemas import UserRead

from .depends import get_current_authenticated_user
from .usecases.login_user import LoginUser

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/login",
    response_model=SuccessResponse[Token],
    summary="Authenticate user and return access token",
    responses={
        200: {"description": "Successful login, returns access token"},
        401: {"description": "Invalid credentials"},
        404: {"description": "User not found"},
        500: {"description": "Internal server error"},
    },
)
async def login(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
):
    email = form_data.username
    password = form_data.password

    user_authenticated_data = await LoginUser(user_repository).execute(email, password)
    result = SuccessResult[Token](
        code=SuccessCodes.SUCCESS,
        message="",
        status_code=status.HTTP_200_OK,
        data=user_authenticated_data
    )
    return result.to_json_response(request)


@router.get(
    "/me",
    response_model=SuccessResponse[UserRead],
    status_code=status.HTTP_200_OK,
    summary="Get current authenticated user",
)
async def get_current_user(
    request: Request,
    current_user: Annotated[UserRead, Depends(get_current_authenticated_user)],
):
    result = SuccessResult[UserRead](
        code=SuccessCodes.SUCCESS,
        message="User retrieved successfully",
        status_code=status.HTTP_200_OK,
        data=UserRead.model_validate(current_user),
    )
    return result.to_json_response(request)
