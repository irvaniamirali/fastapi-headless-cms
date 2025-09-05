import pytest


@pytest.mark.asyncio
async def test_register_user_duplicate_email(http_client):
    # First registration
    await http_client.post(
        "/v1/users/register",
        json={"email": "duplicate@example.com", "password": "StrongPassword123!"},
    )
    # Duplicate registration
    response = await http_client.post(
        "/v1/users/register",
        json={"email": "duplicate@example.com", "password": "StrongPassword123!"},
    )
    assert response.status_code == 409
    assert response.json()["error"]["message"] == "Email already registered."
