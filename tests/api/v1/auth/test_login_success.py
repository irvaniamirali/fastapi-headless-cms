import pytest


@pytest.mark.asyncio
async def test_login_success(http_client):
    # First register user
    await http_client.post(
        "/v1/users/register",
        json={
            "email": "login@example.com",
            "password": "StrongPassword123!"
        }
    )

    response = await http_client.post(
        "/v1/auth/login",
        data={
            "username": "login@example.com",
            "password": "StrongPassword123!"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
