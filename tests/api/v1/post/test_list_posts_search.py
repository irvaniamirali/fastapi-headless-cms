import pytest


@pytest.mark.asyncio
async def test_list_posts_search(http_client, create_post_fixture):
    await create_post_fixture(title="A post about FastAPI")
    await create_post_fixture(title="Another post")
    await create_post_fixture(title="Something about Python")

    response = await http_client.get("/v1/posts/?search=FastAPI")
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "A post about FastAPI"
