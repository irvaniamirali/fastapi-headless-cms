from app.common.exceptions.app_exceptions import (
    EntityNotFoundException,
    PermissionDeniedException,
    DatabaseOperationException,
)

from ..models import Comment
from ..schemas import CommentOut
from ..repositories import CommentRepositoryInterface


class DeleteComment:

    def __init__(self, comment_repository: CommentRepositoryInterface) -> None:
        self.comment_repository = comment_repository

    async def execute(
        self, *, comment_id: int, requesting_user_id: int, is_superuser: bool = False
    ) -> CommentOut:
        """
        Soft delete a comment by ID.

        Args:
            comment_id (int): ID of the comment to delete.
            requesting_user_id (int): ID of the user performing the deletion.
            is_superuser (bool): Whether the user has superuser privileges.

        Raises:
            EntityNotFoundException: If the comment with the given ID does not exist or is already deleted.
            PermissionDeniedException: If the requesting user is neither the author nor a superuser.
            DatabaseOperationException: If a database operation fails during read or delete.
                Includes {"comment_id": comment_id} in exception data.

        Returns:
            CommentOut: The soft-deleted comment.
        """

        try:
            existing_comment: Comment | None = await self.comment_repository.get_comment_by_id(comment_id)
        except Exception as e:
            raise DatabaseOperationException(
                operation="read",
                message=f"Failed to read comment with id {comment_id}",
                data={"comment_id": comment_id},
            ) from e

        if not existing_comment:
            raise EntityNotFoundException(
                message=f"Comment with id {comment_id} was not found.",
                data={"comment_id": comment_id},
            )

        if existing_comment.is_deleted:
            raise EntityNotFoundException(
                message=f"Comment with id {comment_id} not found or deleted.",
                data={"comment_id": comment_id},
            )

        if existing_comment.author_id != requesting_user_id and not is_superuser:
            raise PermissionDeniedException(
                message="You are not allowed to delete this comment.",
                data={"comment_id": comment_id, "requesting_user_id": requesting_user_id},
            )

        try:
            await self.comment_repository.soft_delete_comment(existing_comment)
        except Exception as e:
            raise DatabaseOperationException(
                operation="delete",
                message=f"Failed to soft delete comment with id {comment_id}",
                data={"comment_id": comment_id},
            ) from e

        return CommentOut.model_validate(existing_comment)
