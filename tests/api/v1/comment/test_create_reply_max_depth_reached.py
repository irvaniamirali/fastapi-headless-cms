import pytest

from app.utils.jwt import create_access_token


@pytest.mark.asyncio
async def test_create_reply_max_depth_reached(http_client, registered_user, create_comment_fixture):
    # Create a chain of comments to reach max depth (3)
    c1 = await create_comment_fixture()
    c2 = await create_comment_fixture(post=c1.post, parent_id=c1.id)
    c3 = await create_comment_fixture(post=c2.post, parent_id=c2.id)

    access_token = create_access_token(registered_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "post_id": c3.post_id,
        "content": "This reply is at depth 4 and should fail.",
        "parent_id": c3.id
    }
    response = await http_client.post("/v1/comments/", json=data, headers=headers)
    assert response.status_code == 422
    assert response.json()["error"]["message"] == "Maximum reply depth reached"
