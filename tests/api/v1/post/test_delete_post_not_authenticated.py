import pytest


@pytest.mark.asyncio
async def test_delete_post_not_authenticated(
    http_client, create_post_fixture, registered_user
):
    post = await create_post_fixture(author=registered_user)
    response = await http_client.delete(f"/v1/posts/{post.id}")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
