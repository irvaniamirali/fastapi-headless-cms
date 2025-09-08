import pytest

from app.common.http_responses.error_response import ErrorCodes
from app.utils.auth.jwt import create_access_token


@pytest.mark.asyncio
async def test_create_post_with_duplicate_slug(http_client, registered_user):
    access_token = create_access_token(registered_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}

    # First post
    data1 = {
        "title": "Unique Title",
        "content": "Content for a unique slug.",
        "slug": "unique-slug",
    }
    response1 = await http_client.post("/v1/posts/", json=data1, headers=headers)
    assert response1.status_code == 201

    # Second post with same slug, should raise ConflictException
    data2 = {
        "title": "Another Unique Title",
        "content": "Content for a second post with a unique slug.",
        "slug": "unique-slug",
    }
    response2 = await http_client.post("/v1/posts/", json=data2, headers=headers)

    assert response2.status_code == 409
    post_data = response2.json()
    assert post_data["detail"]["code"] == ErrorCodes.DUPLICATE_ENTRY
    assert "already exists." in post_data["detail"]["message"]
