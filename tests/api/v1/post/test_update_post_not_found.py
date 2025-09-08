import pytest

from app.utils.auth.jwt import create_access_token


@pytest.mark.asyncio
async def test_update_post_not_found(http_client, registered_user):
    access_token = create_access_token(registered_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}
    update_data = {"title": "Nonexistent Post"}

    post_id = 99999
    response = await http_client.patch(
        f"/v1/posts/{post_id}", json=update_data, headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"]["message"] == f"Post with id {post_id} not found."
