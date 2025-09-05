import pytest

from app.utils.jwt import create_access_token


@pytest.mark.asyncio
async def test_create_comment_success(http_client, registered_user, create_post_fixture):
    post = await create_post_fixture()
    access_token = create_access_token(registered_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "post_id": post.id,
        "content": "This is a new comment."
    }
    response = await http_client.post("/v1/comments/", json=data, headers=headers)
    assert response.status_code == 201
    comment_data = response.json()
    assert comment_data["content"] == data["content"]
    assert comment_data["author_id"] == registered_user.id
    assert "replies" in comment_data
    assert len(comment_data["replies"]) == 0
