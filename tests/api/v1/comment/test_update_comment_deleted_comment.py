import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.comment.repositories.comment import CommentRepository
from app.utils.auth.jwt import create_access_token


@pytest.mark.asyncio
async def test_update_comment_deleted_comment(
    http_client, registered_user, create_comment_fixture, db_session: AsyncSession
):
    comment = await create_comment_fixture(author=registered_user)

    # Soft delete the comment
    comment_repository = CommentRepository(db_session)
    await comment_repository.soft_delete_comment(comment)

    access_token = create_access_token(registered_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}
    update_data = {"content": "Attempt to update deleted comment."}

    response = await http_client.patch(
        f"/v1/comments/{comment.id}", json=update_data, headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"]["message"] == f"Comment with id {comment.id} not found."
