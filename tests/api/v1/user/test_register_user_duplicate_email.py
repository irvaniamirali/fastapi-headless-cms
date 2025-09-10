import pytest


@pytest.mark.asyncio
async def test_register_user_duplicate_email(http_client):
    # First registration
    duplicate_user_data = {"email": "duplicate@example.com", "password": "StrongPassword123!"}
    await http_client.post(
        "/v1/users/register", json=duplicate_user_data,
    )
    # Duplicate registration
    response = await http_client.post(
        "/v1/users/register",
        json=duplicate_user_data
    )
    assert response.status_code == 409
    assert response.json()["detail"]["message"] == f"email '{duplicate_user_data["email"]}' already exists."
