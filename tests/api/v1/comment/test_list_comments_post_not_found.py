import pytest


@pytest.mark.asyncio
async def test_list_comments_post_not_found(http_client):
    comment_id = 99999
    response = await http_client.get(f"/v1/comments/post/{comment_id}")
    assert response.status_code == 404
    assert response.json()["detail"]["message"] == f"Post with id {comment_id} not found."
