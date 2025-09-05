import pytest


@pytest.mark.asyncio
async def test_list_comments_success(http_client, create_comment_fixture, create_post_fixture):
    post = await create_post_fixture()
    await create_comment_fixture(post=post)
    await create_comment_fixture(post=post)
    response = await http_client.get(f"/v1/comments/post/{post.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
