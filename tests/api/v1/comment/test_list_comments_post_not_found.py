import pytest


@pytest.mark.asyncio
async def test_list_comments_post_not_found(http_client):
    response = await http_client.get("/v1/comments/post/99999")
    assert response.status_code == 404
    assert response.json()["error"]["message"] == "Post not found"
