import pytest


@pytest.mark.asyncio
async def test_create_comment_not_authenticated(http_client, create_post_fixture):
    post = await create_post_fixture()
    data = {"post_id": post.id, "content": "This should fail."}
    response = await http_client.post("/v1/comments/", json=data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
