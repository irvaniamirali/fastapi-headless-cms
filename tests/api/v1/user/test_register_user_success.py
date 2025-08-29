import pytest
from httpx import AsyncClient

from app.domain.user.models import UserRole


@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient):
    """Test user registration with valid data."""
    user_data = {
        "email": "test_user_1@example.com",
        "password": "ValidPassword123"
    }
    response = await client.post("/v1/users/", json=user_data)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["code"] == "CREATED"
    assert data["message"] == "User created successfully"
    assert "id" in data["data"]
    assert data["data"]["email"] == user_data["email"]
    assert data["data"]["role"] == UserRole.USER.name
    assert data["data"]["is_active"] is True
