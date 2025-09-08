import pytest

from app.utils.auth.jwt import create_access_token


@pytest.mark.asyncio
async def test_update_post_by_different_user(
    http_client, create_post_fixture, registered_user, registered_user2
):
    post = await create_post_fixture(author=registered_user)
    access_token = create_access_token(registered_user2.email)
    headers = {"Authorization": f"Bearer {access_token}"}

    update_data = {"title": "Attempt to Update by different user"}
    response = await http_client.patch(
        f"/v1/posts/{post.id}", json=update_data, headers=headers
    )

    assert response.status_code == 403
    assert response.json()["detail"]["message"] == "You are not allowed to edit this post."
