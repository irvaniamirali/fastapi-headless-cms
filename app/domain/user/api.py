from typing import Annotated

from fastapi import APIRouter, Depends, Request, status

from app.common.http_response.doc_reponses import ResponseErrorDoc, ResponseSuccessDoc
from app.common.http_response.success_response import SuccessCodes, SuccessResponse
from app.common.http_response.success_result import SuccessResult

from .depends import get_user_repository
from .repositories.interface import UserRepositoryInterface
from .schemas import UserCreate, UserRead
from .usecases.register import RegisterUser

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/",
    response_model=SuccessResponse[UserRead],
    status_code=status.HTTP_201_CREATED,
    responses={
        **ResponseSuccessDoc.HTTP_201_CREATED("User created successfully", UserRead),
        **ResponseErrorDoc.HTTP_409_CONFLICT("User already exists"),
    },
)
async def register(
        request: Request,
        user_schema: UserCreate,
        user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
):
    usecase = RegisterUser(user_repository)
    user_register = await usecase.execute(user_schema)

    response = SuccessResult[UserRead](
        code=SuccessCodes.CREATED,
        message="User created successfully",
        status_code=status.HTTP_201_CREATED,
        data=user_register
    )

    return response.to_json_response(request)
