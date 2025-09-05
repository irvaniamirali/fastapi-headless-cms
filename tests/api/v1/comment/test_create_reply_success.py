import pytest

from app.utils.jwt import create_access_token


@pytest.mark.asyncio
async def test_create_reply_success(http_client, registered_user, create_comment_fixture):
    parent_comment = await create_comment_fixture(content="Parent comment.")
    access_token = create_access_token(registered_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "post_id": parent_comment.post_id,
        "content": "This is a reply.",
        "parent_id": parent_comment.id
    }
    response = await http_client.post("/v1/comments/", json=data, headers=headers)
    assert response.status_code == 201
    reply_data = response.json()
    assert reply_data["parent_id"] == parent_comment.id
