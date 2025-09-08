import pytest

from app.utils.auth.jwt import create_access_token


@pytest.mark.asyncio
async def test_delete_comment_not_found(http_client, registered_user):
    access_token = create_access_token(registered_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}
    comment_id = 99999
    response = await http_client.delete(f"/v1/comments/{comment_id}", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"]["message"] == f"Comment with id {comment_id} was not found."
