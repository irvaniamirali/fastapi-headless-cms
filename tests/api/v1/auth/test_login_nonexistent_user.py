import pytest


@pytest.mark.asyncio
async def test_login_nonexistent_user(http_client):
    response = await http_client.post(
        "/v1/auth/login",
        data={"username": "notfound@example.com", "password": "AnyPassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"]["message"] == "Authentication failed"
