import pytest


@pytest.mark.asyncio
async def test_get_post_with_invalid_slug_format(http_client):
    slug = "invalid_slug!"
    response = await http_client.get(f"/v1/posts/{slug}")
    assert response.status_code == 404
    assert response.json()["detail"]["message"] == f"Post with id or slug '{slug}' not found."
