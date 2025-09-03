import pytest


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(http_client):
    response = await http_client.get(
        "/v1/auth/me",
        headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate authentication credentials"
