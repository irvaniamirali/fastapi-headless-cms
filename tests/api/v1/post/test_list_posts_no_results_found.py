import pytest


@pytest.mark.asyncio
async def test_list_posts_no_results_found(http_client):
    response = await http_client.get("/v1/posts/?search=nonexistent_search")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert len(data["items"]) == 0
