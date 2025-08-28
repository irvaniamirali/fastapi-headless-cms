from typing import Annotated

from fastapi import Depends, APIRouter, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from app.common.http_response.doc_reponses import ResponseErrorDoc, ResponseSuccessDoc
from app.common.http_response.success_response import SuccessCodes, SuccessResponse
from app.common.http_response.success_result import SuccessResult
from app.domain.user.depends import get_user_repository
from app.domain.user.models import UserRole
from app.domain.user.repositories.interface import UserRepositoryInterface
from app.domain.user.schemas import UserRead

from .depends import get_current_authenticated_user
from .schemas import (
    JWTPayload,
    OAuth2TokenResponse,
    TokenResponse,
    TokenType,
    TokenRefresh,
    TokenAccess
)
from .usecases.authenticate import AuthenticateUser
from .usecases.create_tokens import CreateTokens
from .usecases.read_jwt_token import ReadJwtToken
from .usecases.verify_token_payload import VerifyTokenPayload

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses=ResponseErrorDoc.HTTP_404_NOT_FOUND("NOT FOUND"),
)


@router.post(
    "/token",
    description="Authenticate a user with email and password, then return a JWT access token and refresh token.",
    response_model=SuccessResponse[TokenResponse],
    status_code=status.HTTP_201_CREATED,
    responses={
        **ResponseSuccessDoc.HTTP_201_CREATED("Token created successfully", TokenResponse),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR("Operation Failure"),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND("Entity not found"),
        **ResponseErrorDoc.HTTP_403_FORBIDDEN("UNACCESSIBLE"),
        **ResponseErrorDoc.HTTP_401_UNAUTHORIZED("Invalid credentials"),
    },
)
async def auth_and_token(
        request: Request,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
):
    """
    Authenticate user and provide access token and refresh token.

    Args:
        form_data (OAuth2PasswordRequestForm): Form data containing username and password.
        request (Request): FastAPI request object, used to get the request path.
        user_repository (UserRepositoryInterface): Repository for accessing user data.

    Returns:
        dict | None: Access token and refresh token if authentication is successful, None otherwise.
    """

    email = form_data.username
    password = form_data.password

    user = await AuthenticateUser(user_repository).execute(email, password)

    user_role = str(UserRole(user.role).name.lower())

    create_tokens = CreateTokens(user_id=str(user.id), user_role=user_role)
    tokens = await create_tokens.execute()

    result = SuccessResult[TokenResponse](
        code=SuccessCodes.CREATED,
        message="Tokens created successfully",
        status_code=status.HTTP_201_CREATED,
        data=tokens,
    )

    return result.to_json_response(request)


@router.post(
    "/token/swagger",
    response_model=OAuth2TokenResponse,
    include_in_schema=True,
    summary="OAuth2 Token for Swagger UI",
    description="This endpoint is used to obtain an OAuth2 token for Swagger UI.",
    status_code=status.HTTP_200_OK,
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("Token retrieved successfully", OAuth2TokenResponse),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR("Operation Failure"),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND("Entity not found"),
        **ResponseErrorDoc.HTTP_403_FORBIDDEN("UNACCESSIBLE"),
        **ResponseErrorDoc.HTTP_401_UNAUTHORIZED("Invalid credentials"),
    },
)
async def auth_swagger_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        user_repository: UserRepositoryInterface = Depends(get_user_repository),
):
    """
    Swagger UI token endpoint.
    This endpoint is used to obtain an OAuth2 token for Swagger UI.
    Args:
        form_data (OAuth2PasswordRequestForm): Form data containing username and password.
        user_repository (UserRepositoryInterface): User repository dependency.
    Returns:
        dict: Access token and token type.
    """

    user = await AuthenticateUser(user_repository).execute(form_data.username, form_data.password)
    user_role = str(UserRole(user.role).name.lower())

    tokens = await CreateTokens(user_id=str(user.id), user_role=user_role).execute()

    return {"access_token": tokens.access_token, "token_type": "bearer"}


@router.get(
    "/me",
    description="Get current user information",
    response_model=SuccessResponse[UserRead],
    status_code=status.HTTP_200_OK,
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("User retrieved successfully", UserRead),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR("Operation Failure"),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND("Entity not found"),
        **ResponseErrorDoc.HTTP_403_FORBIDDEN("UNACCESSIBLE"),
        **ResponseErrorDoc.HTTP_401_UNAUTHORIZED("Invalid credentials"),
    },
)
async def get_current_user(
        request: Request,
        user: Annotated[UserRead, Depends(get_current_authenticated_user)],
):
    """
    Get current user information.
    This endpoint retrieves the information of the currently authenticated user.
    Args:
        request (Request): The FastAPI request object.
        user (UserRead): The authenticated user object.
    Returns:
        SuccessResponse[UserRead]: A success response containing the user information.
    """

    response = SuccessResult[UserRead](
        code=SuccessCodes.SUCCESS,
        message="User retrieved successfully",
        status_code=status.HTTP_200_OK,
        data=user,
    )
    return response.to_json_response(request)


@router.post(
    "/token/refresh",
    description="Refresh tokens using refresh token",
    response_model=SuccessResponse[TokenResponse],
    status_code=status.HTTP_200_OK,
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("Tokens refreshed successfully", TokenResponse),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR("Operation Failure"),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND("Entity not found"),
        **ResponseErrorDoc.HTTP_403_FORBIDDEN("UNACCESSIBLE"),
        **ResponseErrorDoc.HTTP_401_UNAUTHORIZED("Invalid credentials"),
    },
)
async def refresh_tokens(
        request: Request,
        refresh_token: TokenRefresh,
        user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
):
    """
    Refresh tokens using refresh token.
    This endpoint allows the user to refresh their access and refresh tokens.
    Args:
        request (Request): The FastAPI request object.
        refresh_token (TokenRefresh): Refresh token sent by the client.
        user_repository (UserRepositoryInterface): User repository dependency.
    Returns:
        SuccessResponse[TokenResponse]: A success response containing the new tokens.
    """

    payload: JWTPayload = await ReadJwtToken(refresh_token.refresh_token).execute()

    user = await VerifyTokenPayload(user_repository).execute(payload, TokenType.refresh)
    user_role = str(UserRole(user.role).name.lower())

    tokens = await CreateTokens(user_id=str(user.id), user_role=user_role).execute()
    response = SuccessResult[TokenResponse](
        code=SuccessCodes.CREATED,
        message="Tokens created successfully",
        status_code=status.HTTP_201_CREATED,
        data=tokens,
    )

    return response.to_json_response(request)


@router.get(
    "/token/verify",
    description="Verify access token",
    response_model=SuccessResponse[TokenResponse],
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("access token verified successfully", TokenResponse),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR("Operation Failure"),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND("Entity not found"),
        **ResponseErrorDoc.HTTP_403_FORBIDDEN("UNACCESSIBLE"),
        **ResponseErrorDoc.HTTP_401_UNAUTHORIZED("Invalid credentials"),
    },
)
async def verify_refresh_token(
        request: Request,
        access_token: TokenAccess,
        user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
):
    """
    Verify access token.
    This endpoint allows the user to verify their access token.
    Args:
        request (Request): The FastAPI request object.
        access_token (TokenAccess): Access token sent by the client.
        user_repository (UserRepositoryInterface): User repository dependency.
    Returns:
        SuccessResponse[TokenResponse]: A success response containing the verified tokens.
    """

    payload: JWTPayload = await ReadJwtToken(access_token.access_token).execute()

    user_read = await VerifyTokenPayload(user_repository).execute(payload, TokenType.access)

    response = SuccessResult[UserRead](
        code=SuccessCodes.SUCCESS,
        message="User is valid",
        status_code=status.HTTP_200_OK,
        data=user_read,
    )

    return response.to_json_response(request)
