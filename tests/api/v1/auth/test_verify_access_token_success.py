import pytest
from httpx import AsyncClient

from tests.conftest import MOCK_USER_EMAIL, MOCK_USER_PASSWORD, setup_mock_user
from app.domain.user.models import UserRole


@pytest.mark.asyncio
async def test_verify_access_token_success(client: AsyncClient):
    """Test verifying an access token."""
    await setup_mock_user(client, MOCK_USER_EMAIL, MOCK_USER_PASSWORD)
    login_data = {
        "username": MOCK_USER_EMAIL,
        "password": MOCK_USER_PASSWORD
    }
    login_response = await client.post("/v1/auth/token", data=login_data)
    assert login_response.status_code == 201
    access_token = login_response.json()["data"]["access_token"]

    verify_response = await client.get("/v1/auth/token/verify", params={"access_token": access_token})
    print(verify_response)
    assert verify_response.status_code == 200
    data = verify_response.json()["data"]
    assert data["email"] == MOCK_USER_EMAIL
    assert data["role"] == UserRole.USER
