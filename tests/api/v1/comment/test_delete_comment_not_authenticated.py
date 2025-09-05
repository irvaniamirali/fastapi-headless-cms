import pytest


@pytest.mark.asyncio
async def test_delete_comment_not_authenticated(http_client, create_comment_fixture):
    comment = await create_comment_fixture()
    response = await http_client.delete(f"/v1/comments/{comment.id}")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
