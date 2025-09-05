import pytest

from app.utils.jwt import create_access_token


@pytest.mark.asyncio
async def test_create_comment_post_not_found(http_client, registered_user):
    access_token = create_access_token(registered_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "post_id": 99999,
        "content": "Comment on a nonexistent post."
    }
    response = await http_client.post("/v1/comments/", json=data, headers=headers)
    assert response.status_code == 404
    assert response.json()["error"]["message"] == "Post not found"
