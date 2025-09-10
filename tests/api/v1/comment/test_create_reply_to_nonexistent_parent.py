import pytest

from app.utils.auth.jwt import create_access_token


@pytest.mark.asyncio
async def test_create_reply_to_nonexistent_parent(
    http_client, registered_user, create_post_fixture
):
    post = await create_post_fixture()
    access_token = create_access_token(registered_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"post_id": post.id, "content": "This should fail.", "parent_id": 99999}
    response = await http_client.post("/v1/comments/", json=data, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"]["message"] == f"Parent comment with id {data["parent_id"]} was not found."
