from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from app.utils.jwt import create_access_token
from app.domain.comment.repositories.comment import CommentRepository


@pytest.mark.asyncio
async def test_update_comment_deleted_comment(
        http_client, registered_user, create_comment_fixture, db_session: AsyncSession
):
    comment = await create_comment_fixture(author=registered_user)

    # Soft delete the comment
    comment_repository = CommentRepository(db_session)
    await comment_repository.delete(comment)

    access_token = create_access_token(registered_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}
    update_data = {"content": "Attempt to update deleted comment."}

    response = await http_client.patch(f"/v1/comments/{comment.id}", json=update_data, headers=headers)

    assert response.status_code == 404
    assert response.json()["error"]["message"] == "Comment not found"
