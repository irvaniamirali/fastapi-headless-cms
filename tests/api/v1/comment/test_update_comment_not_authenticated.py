import pytest


@pytest.mark.asyncio
async def test_update_comment_not_authenticated(http_client, create_comment_fixture):
    comment = await create_comment_fixture()
    update_data = {"content": "Attempt to update."}
    response = await http_client.patch(f"/v1/comments/{comment.id}", json=update_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
