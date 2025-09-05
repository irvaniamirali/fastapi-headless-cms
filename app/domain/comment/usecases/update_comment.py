from app.core.exceptions.app_exceptions import (
    NotFoundException,
    PermissionDeniedException,
    ConflictException,
)

from ..repositories import CommentRepositoryInterface
from ..schemas import CommentOut


class UpdateComment:
    """
    Use case for updating a comment's content.

    Ensures the comment exists, is not deleted, and the actor has permission.
    """

    def __init__(self, comment_repository: CommentRepositoryInterface):
        self.comment_repository = comment_repository

    async def execute(
        self,
        *,
        comment_id: int,
        content: str,
        actor_id: int,
        is_superuser: bool = False,
    ) -> CommentOut:
        """
        Update a comment's content.

        Args:
            comment_id (int): ID of the comment to update.
            content (str): New content for the comment.
            actor_id (int): ID of the user attempting the update.
            is_superuser (bool): Whether the actor has superuser privileges.

        Raises:
            NotFoundException: If the comment does not exist.
            ConflictException: If the comment is deleted.
            PermissionDeniedException: If the actor is not allowed to edit.

        Returns:
            CommentOut: The updated comment as an output schema.
        """

        comment = await self.comment_repository.get_by_id(comment_id)

        if not comment:
            raise NotFoundException("Comment not found")

        if comment.is_deleted:
            raise ConflictException("Cannot edit a deleted comment")

        if comment.author_id != actor_id and not is_superuser:
            raise PermissionDeniedException("Not allowed to edit this comment")

        updated = await self.comment_repository.update(comment, content)

        return CommentOut(
            id=updated.id,
            post_id=updated.post_id,
            author_id=updated.author_id,
            content=updated.content,
            parent_id=updated.parent_id,
            replies=[],
        )
