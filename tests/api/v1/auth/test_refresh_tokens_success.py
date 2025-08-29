import pytest
from httpx import AsyncClient

from tests.conftest import MOCK_USER_EMAIL, MOCK_USER_PASSWORD, setup_mock_user
from app.core.config import settings


@pytest.mark.asyncio
async def test_refresh_tokens_success(client: AsyncClient):
    """Test refreshing tokens using a refresh token."""
    await setup_mock_user(client, MOCK_USER_EMAIL, MOCK_USER_PASSWORD)
    login_data = {
        "username": MOCK_USER_EMAIL,
        "password": MOCK_USER_PASSWORD
    }
    login_response = await client.post("/v1/auth/token", data=login_data)
    assert login_response.status_code == 201
    refresh_token = login_response.json()["data"]["refresh_token"]

    refresh_response = await client.post("/v1/auth/token/refresh", json={"refresh_token": refresh_token})
    assert refresh_response.status_code == 201
    data = refresh_response.json()["data"]
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["access_token_expire_in"] == settings.ACCESS_TOKEN_EXPIRE_SECONDS
    assert data["refresh_token_expire_in"] == settings.REFRESH_TOKEN_EXPIRE_SECONDS
