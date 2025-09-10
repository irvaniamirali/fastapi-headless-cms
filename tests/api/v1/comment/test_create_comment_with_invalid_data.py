import pytest

from app.utils.auth.jwt import create_access_token


@pytest.mark.asyncio
async def test_create_comment_with_invalid_data(
    http_client, registered_user, create_post_fixture
):
    post = await create_post_fixture()
    access_token = create_access_token(registered_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"post_id": post.id, "content": ""}
    response = await http_client.post("/v1/comments/", json=data, headers=headers)
    assert response.status_code == 422
