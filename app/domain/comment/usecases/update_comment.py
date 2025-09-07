from app.core.exceptions.app_exceptions import (
    ConflictException,
    NotFoundException,
    PermissionDeniedException,
)

from ..models import Comment
from ..repositories import CommentRepositoryInterface
from ..schemas import CommentOut


class UpdateComment:
    """
    Use case for updating a comment's content.

    Ensures the comment exists, is not deleted, and the actor has permission.
    """

    def __init__(self, comment_repository: CommentRepositoryInterface) -> None:
        self.comment_repository = comment_repository

    async def execute(
        self,
        *,
        comment_id: int,
        new_content: str,
        requesting_user_id: int,
        is_superuser: bool = False,
    ) -> CommentOut:
        """
        Update a comment's content.

        Args:
            comment_id (int): ID of the comment to update.
            new_content (str): New content for the comment.
            requesting_user_id (int): ID of the user attempting the update.
            is_superuser (bool): Whether the actor has superuser privileges.

        Raises:
            NotFoundException: If the comment does not exist.
            ConflictException: If the comment is deleted.
            PermissionDeniedException: If the actor is not allowed to edit.

        Returns:
            CommentOut: The updated comment as an output schema.
        """

        existing_comment: Comment | None = (
            await self.comment_repository.get_comment_by_id(comment_id)
        )

        if not existing_comment:
            raise NotFoundException("Comment not found")

        if existing_comment.is_deleted:
            raise ConflictException("Cannot edit a deleted comment")

        if existing_comment.author_id != requesting_user_id and not is_superuser:
            raise PermissionDeniedException("Not allowed to edit this comment")

        updated_comment: Comment = await self.comment_repository.update_comment_content(
            existing_comment, new_content
        )

        return CommentOut.model_validate(updated_comment)
