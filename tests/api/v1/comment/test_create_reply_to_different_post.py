import pytest

from app.utils.jwt import create_access_token


@pytest.mark.asyncio
async def test_create_reply_to_different_post(
    http_client, registered_user, create_comment_fixture, create_post_fixture
):
    post1 = await create_post_fixture()
    post2 = await create_post_fixture()
    parent_comment = await create_comment_fixture(post=post1)
    access_token = create_access_token(registered_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "post_id": post2.id,
        "content": "This should fail.",
        "parent_id": parent_comment.id,
    }
    response = await http_client.post("/v1/comments/", json=data, headers=headers)
    assert response.status_code == 403
    assert (
        response.json()["error"]["message"]
        == "Parent comment belongs to a different post"
    )
