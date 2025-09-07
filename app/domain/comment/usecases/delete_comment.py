from app.core.exceptions.app_exceptions import (
    ConflictException,
    NotFoundException,
    PermissionDeniedException,
)

from ..models import Comment
from ..repositories import CommentRepositoryInterface


class DeleteComment:
    """
    Use case for deleting a comment (soft delete).

    Ensures the comment exists, checks actor permissions,
    and marks the comment as deleted.
    """

    def __init__(self, comment_repository: CommentRepositoryInterface) -> None:
        self.comment_repository = comment_repository

    async def execute(
        self, *, comment_id: int, requesting_user_id: int, is_superuser: bool = False
    ) -> None:
        """
        Soft delete a comment by ID.

        Args:
            comment_id (int): The ID of the comment to delete.
            requesting_user_id (int): The ID of the user attempting the deletion.
            is_superuser (bool): Whether the actor has superuser privileges.

        Raises:
            NotFoundException: If the comment does not exist.
            PermissionDeniedException: If the actor is not allowed to delete it.
            ConflictException: If the comment is already deleted.
        """

        existing_comment: Comment | None = (
            await self.comment_repository.get_comment_by_id(comment_id)
        )

        if not existing_comment:
            raise NotFoundException("Comment not found")

        if existing_comment.is_deleted:
            raise ConflictException("Comment is already deleted")

        if existing_comment.author_id != requesting_user_id and not is_superuser:
            raise PermissionDeniedException("Not allowed to delete this comment")

        await self.comment_repository.soft_delete_comment(existing_comment)
