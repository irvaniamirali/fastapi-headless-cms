import pytest

from app.utils.jwt import create_access_token


@pytest.mark.asyncio
async def test_delete_comment_success(http_client, registered_user, create_comment_fixture):
    comment = await create_comment_fixture(author=registered_user)
    access_token = create_access_token(registered_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await http_client.delete(f"/v1/comments/{comment.id}", headers=headers)
    assert response.status_code == 204
