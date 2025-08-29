import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_current_user_unauthorized_failure(client: AsyncClient):
    """Test retrieving user info without a token."""
    response = await client.get("/v1/auth/me")
    assert response.status_code == 401
    data = response.json()["detail"]
    assert data == "Not authenticated"
