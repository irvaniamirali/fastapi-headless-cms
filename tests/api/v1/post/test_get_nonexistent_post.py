import pytest


@pytest.mark.asyncio
async def test_get_nonexistent_post(http_client):
    response = await http_client.get("/v1/posts/99999")
    assert response.status_code == 404
    assert response.json()["error"]["message"] == "Post not found"
