import pytest


@pytest.mark.asyncio
async def test_list_posts_success(http_client, create_post_fixture):
    # Create multiple posts
    await create_post_fixture(title="Post A")
    await create_post_fixture(title="Post B")
    await create_post_fixture(title="Post C")

    response = await http_client.get("/v1/posts/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 3
    assert len(data["items"]) >= 3
