import pytest


@pytest.mark.asyncio
async def test_update_post_not_authenticated(http_client, create_post_fixture, registered_user):
    post = await create_post_fixture(author=registered_user)
    update_data = {"title": "Attempt to Update"}
    response = await http_client.patch(f"/v1/posts/{post.id}", json=update_data)

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
