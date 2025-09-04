import pytest


@pytest.mark.asyncio
async def test_get_post_by_slug_success(http_client, create_post_fixture):
    post = await create_post_fixture(title="Test Post By Slug")
    response = await http_client.get(f"/v1/posts/{post.slug}")
    assert response.status_code == 200
    post_data = response.json()
    assert post_data["title"] == "Test Post By Slug"
    assert post_data["slug"] == post.slug
