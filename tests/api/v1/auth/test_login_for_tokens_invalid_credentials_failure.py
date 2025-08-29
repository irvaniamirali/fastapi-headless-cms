import pytest
from httpx import AsyncClient

from tests.conftest import MOCK_USER_EMAIL, MOCK_USER_PASSWORD, setup_mock_user


@pytest.mark.asyncio
async def test_login_for_tokens_invalid_credentials_failure(client: AsyncClient):
    """Test login with invalid password."""
    await setup_mock_user(client, MOCK_USER_EMAIL, MOCK_USER_PASSWORD)
    login_data = {
        "username": MOCK_USER_EMAIL,
        "password": "wrong_password"
    }
    response = await client.post("/v1/auth/token", data=login_data)
    assert response.status_code == 401
    data = response.json()["detail"]
    assert data["code"] == "INVALID_CREDENTIALS"
    assert data["message"] == "Invalid credentials"
