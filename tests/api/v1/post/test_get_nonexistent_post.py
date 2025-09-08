import pytest


@pytest.mark.asyncio
async def test_get_nonexistent_post(http_client):
    post_id = 99999
    response = await http_client.get(f"/v1/posts/{post_id}")
    assert response.status_code == 404
    assert response.json()["detail"]["message"] == f"Post with id or slug '{post_id}' not found."
