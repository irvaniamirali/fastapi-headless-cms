import uuid

import pytest

from app.utils.jwt import create_access_token


@pytest.mark.asyncio
async def test_get_current_user_success(http_client):
    unique_email = f"currentuser_{uuid.uuid4()}@example.com"
    # Register user
    await http_client.post(
        "/v1/users/register",
        json={
            "email": unique_email,
            "password": "StrongPassword123!"
        }
    )

    access_token = create_access_token(unique_email)

    response = await http_client.get(
        "/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == unique_email
