from app.common.exceptions.app_exceptions import InvalidPayloadException
from app.domain.auth.schemas import JWTPayload, TokenResponse, TokenType
from app.core.jwt_handler import JWTHandler

from app.core.config import settings


class CreateTokens:
    def __init__(self, user_id: str, user_role: str) -> None:
        self.sub = user_id
        self.role = user_role

    async def execute(self) -> TokenResponse | None:
        # * create access-token
        payload_access_token: JWTPayload = JWTPayload.create(
            sub=str(self.sub),
            role=self.role,
            token_type=TokenType.access,
            issuer=settings.JWT_ISSUER_SERVER,
            expire_in=settings.ACCESS_TOKEN_EXPIRE_SECONDS,
        )

        try:
            access_token = JWTHandler.create_token(payload_access_token.model_dump())
        except (ValueError, TypeError) as e:
            raise InvalidPayloadException(
                message=f"Failed to create access token, {e}", payload=payload_access_token.model_dump()
            ) from e

        # * create refresh-token
        payload_refresh_token: JWTPayload = JWTPayload.create(
            sub=str(self.sub),
            role=self.role,
            token_type=TokenType.refresh,
            issuer=settings.JWT_ISSUER_SERVER,
            expire_in=settings.REFRESH_TOKEN_EXPIRE_SECONDS,
        )

        try:
            refresh_token = JWTHandler.create_token(payload_refresh_token.model_dump())
        except (ValueError, TypeError) as e:
            raise InvalidPayloadException(
                message=f"Failed to create refresh token, {e}", payload=refresh_token.model_dump()
            ) from e

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            access_token_expire_in=settings.ACCESS_TOKEN_EXPIRE_SECONDS,
            refresh_token_expire_in=settings.REFRESH_TOKEN_EXPIRE_SECONDS,
        )
