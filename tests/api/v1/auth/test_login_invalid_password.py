import pytest
import uuid


@pytest.mark.asyncio
async def test_login_invalid_password(http_client):
    unique_email = f"wrongpass_{uuid.uuid4()}@example.com"
    # Register user
    await http_client.post(
        "/v1/users/register",
        json={"email": unique_email, "password": "CorrectPassword123!"},
    )

    response = await http_client.post(
        "/v1/auth/login", data={"username": unique_email, "password": "WrongPassword"}
    )
    assert response.status_code == 401
    assert response.json()["error"]["message"] == "Invalid credentials"
