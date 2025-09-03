import pytest


@pytest.mark.asyncio
async def test_login_invalid_password(http_client):
    # Register user
    await http_client.post(
        "/v1/users/register",
        data={
            "username": "wrongpass@example.com",
            "password": "CorrectPassword123!"
        }
    )

    response = await http_client.post(
        "/v1/auth/login",
        data={
            "username": "wrongpass@example.com",
            "password": "WrongPassword"
        }
    )
    assert response.status_code == 401
    assert response.json()["error"]["message"] == "Invalid credentials"
