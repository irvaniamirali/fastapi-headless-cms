import pytest

from app.utils.jwt import create_access_token


@pytest.mark.asyncio
async def test_update_post_not_found(http_client, registered_user):
    access_token = create_access_token(registered_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}
    update_data = {"title": "Nonexistent Post"}

    response = await http_client.patch(
        "/v1/posts/99999", json=update_data, headers=headers
    )

    assert response.status_code == 404
    assert response.json()["error"]["message"] == "Post not found"
