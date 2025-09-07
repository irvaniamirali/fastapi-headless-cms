import pytest

from app.utils.jwt import create_access_token


@pytest.mark.asyncio
async def test_update_post_success(http_client, create_post_fixture, registered_user):
    post = await create_post_fixture(title="Original Title", author=registered_user)
    access_token = create_access_token(registered_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}

    update_data = {"title": "Updated Title", "content": "Updated content"}
    response = await http_client.patch(
        f"/v1/posts/{post.id}", json=update_data, headers=headers
    )

    assert response.status_code == 200
    updated_post = response.json()
    assert updated_post["title"] == "Updated Title"
    assert updated_post["content"] == "Updated content"
