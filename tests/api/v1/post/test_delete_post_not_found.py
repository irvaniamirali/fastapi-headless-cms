import pytest

from app.utils.jwt import create_access_token


@pytest.mark.asyncio
async def test_delete_post_not_found(http_client, registered_user):
    access_token = create_access_token(registered_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await http_client.delete("/v1/posts/99999", headers=headers)

    assert response.status_code == 404
    assert response.json()["error"]["message"] == "Post not found"
