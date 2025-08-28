from app.common.exceptions.app_exceptions import InvalidPayloadException
from app.domain.auth.schemas import JWTPayload
from app.core.jwt_handler import JWTHandler


class ReadJwtToken:
    def __init__(self, token: str) -> None:
        self.token = token

    async def execute(self) -> JWTPayload:
        """
        Decode the access token and return the payload.

        Returns:
            JWTPayload: The decoded payload of the access token.
        """

        try:
            payload = JWTHandler.read_token(self.token)
            return JWTPayload.model_validate(payload)
        except Exception as e:
            raise InvalidPayloadException(message=f"Failed to decode  token, {e}", payload=self.token)
