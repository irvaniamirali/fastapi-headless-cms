import pytest

from app.utils.auth.jwt import create_access_token


@pytest.mark.asyncio
async def test_create_post_with_invalid_data(http_client, registered_user):
    access_token = create_access_token(registered_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}
    # Missing title and content
    data = {"title": "", "content": ""}
    response = await http_client.post("/v1/posts/", json=data, headers=headers)
    assert response.status_code == 422
