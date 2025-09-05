import pytest

from app.utils.jwt import create_access_token


@pytest.mark.asyncio
async def test_delete_comment_by_different_user(http_client, registered_user, registered_user2, create_comment_fixture):
    comment = await create_comment_fixture(author=registered_user)
    access_token = create_access_token(registered_user2.email)
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await http_client.delete(f"/v1/comments/{comment.id}", headers=headers)
    assert response.status_code == 403
    assert response.json()["error"]["message"] == "Not allowed to delete this comment"
