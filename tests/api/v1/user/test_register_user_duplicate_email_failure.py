import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user_duplicate_email_failure(client: AsyncClient):
    """Test user registration with a duplicate email."""
    user_data = {
        "email": "duplicate@example.com",
        "password": "Password123"
    }
    await client.post("/v1/users/", json=user_data)
    response = await client.post("/v1/users/", json=user_data)
    assert response.status_code == 409
    data = response.json()
    assert data["detail"]["code"] == "DUPLICATE_ENTRY"
    assert data["detail"]["message"] == "email 'duplicate@example.com' already exists."
