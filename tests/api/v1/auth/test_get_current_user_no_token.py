import pytest


@pytest.mark.asyncio
async def test_get_current_user_no_token(http_client):
    response = await http_client.get("/v1/auth/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
