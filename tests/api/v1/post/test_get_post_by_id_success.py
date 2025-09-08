import pytest


@pytest.mark.asyncio
async def test_get_post_by_id_success(http_client, create_post_fixture):
    post = await create_post_fixture(title="Test Post By ID")
    response = await http_client.get(f"/v1/posts/{post.id}")
    assert response.status_code == 200
    post_data = response.json()["data"]
    assert post_data["title"] == "Test Post By ID"
    assert post_data["id"] == post.id
