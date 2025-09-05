import pytest


@pytest.mark.asyncio
async def test_list_comments_pagination(http_client, create_comment_fixture, create_post_fixture):
    post = await create_post_fixture()
    for _ in range(5):
        await create_comment_fixture(post=post)
    response = await http_client.get(f"/v1/comments/post/{post.id}?limit=2&skip=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
