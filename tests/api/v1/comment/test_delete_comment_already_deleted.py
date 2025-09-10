import pytest

from app.utils.auth.jwt import create_access_token


@pytest.mark.asyncio
async def test_delete_comment_already_deleted(
    http_client, registered_user, create_comment_fixture
):
    comment = await create_comment_fixture(author=registered_user)

    # First delete
    access_token = create_access_token(registered_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}
    await http_client.delete(f"/v1/comments/{comment.id}", headers=headers)

    # Second delete should fail with a 404, not a 409
    response = await http_client.delete(f"/v1/comments/{comment.id}", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"]["message"] == f"Comment with id {comment.id} was not found."
