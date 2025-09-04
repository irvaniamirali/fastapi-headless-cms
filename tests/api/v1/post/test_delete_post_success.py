import pytest

from app.utils.jwt import create_access_token


@pytest.mark.asyncio
async def test_delete_post_success(http_client, create_post_fixture, registered_user):
    post = await create_post_fixture(author=registered_user)
    access_token = create_access_token(registered_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await http_client.delete(f"/v1/posts/{post.id}", headers=headers)
    assert response.status_code == 204
    assert response.text == ""
