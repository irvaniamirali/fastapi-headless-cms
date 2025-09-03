import pytest


@pytest.mark.asyncio
async def test_register_user_success(http_client):
    response = await http_client.post(
        "/v1/users/register",
        json={
            "email": "test@example.com",
            "password": "StrongPassword123!"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "email" in data
    assert data["email"] == "test@example.com"
