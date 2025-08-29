import pytest
from httpx import AsyncClient

from tests.conftest import MOCK_USER_EMAIL, MOCK_USER_PASSWORD, setup_mock_user


@pytest.mark.asyncio
async def test_swagger_oauth2_token_success(client: AsyncClient):
    """Test the Swagger OAuth2 token endpoint."""
    await setup_mock_user(client, MOCK_USER_EMAIL, MOCK_USER_PASSWORD)
    login_data = {
        "username": MOCK_USER_EMAIL,
        "password": MOCK_USER_PASSWORD
    }
    response = await client.post("/v1/auth/token/swagger", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
