import pytest


@pytest.mark.asyncio
async def test_list_posts_pagination(http_client, create_post_fixture):
    for i in range(30):
        await create_post_fixture(title=f"Post {i}")

    response = await http_client.get("/v1/posts/?limit=10&skip=0")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 30
    assert len(data["items"]) == 10
