from typing import Annotated

from fastapi import Request, APIRouter, Depends, status

from app.common.http_responses import SuccessResponse, SuccessCodes
from app.common.http_responses.success_result import SuccessResult

from .depends import get_user_repository
from .repositories import UserRepositoryInterface
from .schemas import UserCreate, UserRead
from .usecases.register_user import RegisterUser

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/register",
    response_model=SuccessResponse[UserRead],
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    responses={
        201: {"description": "User successfully created"},
        409: {"description": "Email already registered"},
        500: {"description": "Internal server error"},
    },
)
async def register_user(
    request: Request,
    user_schema: UserCreate,
    user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
):
    user_data = await RegisterUser(user_repository).execute(user_schema)
    result = SuccessResult[UserRead].create(
        code=SuccessCodes.CREATED,
        message="User created successfully",
        status_code=status.HTTP_201_CREATED,
        data=user_data,
    )
    return result.to_json_response(request)
