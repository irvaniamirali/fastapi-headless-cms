import pytest

from app.utils.jwt import create_access_token


@pytest.mark.asyncio
async def test_update_comment_success(
    http_client, registered_user, create_comment_fixture
):
    comment = await create_comment_fixture(author=registered_user)
    access_token = create_access_token(registered_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}
    update_data = {"content": "Updated content"}
    response = await http_client.patch(
        f"/v1/comments/{comment.id}", json=update_data, headers=headers
    )
    assert response.status_code == 200
    updated_comment = response.json()
    assert updated_comment["content"] == update_data["content"]
