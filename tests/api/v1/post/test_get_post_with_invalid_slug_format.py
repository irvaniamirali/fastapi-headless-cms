import pytest


@pytest.mark.asyncio
async def test_get_post_with_invalid_slug_format(http_client):
    response = await http_client.get("/v1/posts/invalid_slug!")
    assert response.status_code == 404
    assert response.json()["error"]["message"] == "Post not found"
