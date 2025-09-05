from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from app.domain.comment.repositories.comment import CommentRepository
from app.utils.jwt import create_access_token


@pytest.mark.asyncio
async def test_create_reply_to_deleted_comment(
    http_client, registered_user, create_comment_fixture, db_session: AsyncSession
):
    parent_comment = await create_comment_fixture(author=registered_user)

    # Soft delete the comment
    comment_repository = CommentRepository(db_session)
    await comment_repository.delete(parent_comment)

    access_token = create_access_token(registered_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "post_id": parent_comment.post_id,
        "content": "This should fail.",
        "parent_id": parent_comment.id,
    }

    response = await http_client.post("/v1/comments/", json=data, headers=headers)

    assert response.status_code == 404
    assert response.json()["error"]["message"] == "Parent comment not found"
