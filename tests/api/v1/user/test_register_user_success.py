import pytest
import uuid


@pytest.mark.asyncio
async def test_register_user_success(http_client):
    unique_email = f"test_success_{uuid.uuid4()}@example.com"
    response = await http_client.post(
        "/v1/users/register",
        json={
            "email": unique_email,
            "password": "StrongPassword123!"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "email" in data
    assert data["email"] == unique_email
