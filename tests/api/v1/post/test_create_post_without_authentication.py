import pytest


@pytest.mark.asyncio
async def test_create_post_without_authentication(http_client):
    data = {
        "title": "Unauthorized post",
        "content": "Content of an unauthorized post.",
    }
    response = await http_client.post("/v1/posts/", json=data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
