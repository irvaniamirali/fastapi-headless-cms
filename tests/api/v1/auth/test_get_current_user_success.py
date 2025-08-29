import pytest
from httpx import AsyncClient

from tests.conftest import MOCK_USER_EMAIL
from app.domain.user.models import UserRole


@pytest.mark.asyncio
async def test_get_current_user_success(auth_user_client: AsyncClient):
    """Test retrieving the current authenticated user's info."""
    response = await auth_user_client.get("/v1/auth/me")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["email"] == MOCK_USER_EMAIL
    assert data["role"] == UserRole.USER
    assert data["is_active"] is True
