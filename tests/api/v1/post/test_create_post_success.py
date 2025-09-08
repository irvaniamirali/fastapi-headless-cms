import pytest

from app.utils.auth.jwt import create_access_token


@pytest.mark.asyncio
async def test_create_post_success(http_client, registered_user):
    access_token = create_access_token(registered_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "title": "My first blog post",
        "content": "This is the content of my first post.",
    }
    response = await http_client.post("/v1/posts/", json=data, headers=headers)
    assert response.status_code == 201
    post_data = response.json()["data"]
    assert post_data["title"] == "My first blog post"
    assert "slug" in post_data
