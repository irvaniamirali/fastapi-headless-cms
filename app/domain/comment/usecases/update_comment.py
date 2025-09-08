from app.common.exceptions import EntityNotFoundException, PermissionDeniedException

from ..models import Comment
from ..repositories import CommentRepositoryInterface
from ..schemas import CommentOut


class UpdateComment:

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
            NotFoundException: If the comment with the given ID does not exist.
                Includes {"comment_id": comment_id} in exception data.
            ConflictException: If the comment has been deleted.
                Includes {"comment_id": comment_id} in exception data.
            PermissionDeniedException: If the actor is neither the author nor a superuser.
                Includes {"comment_id": comment_id, "requesting_user_id": requesting_user_id} in exception data.

        Returns:
            CommentOut: The updated comment.
        """

        existing_comment: Comment | None = (
            await self.comment_repository.get_comment_by_id(comment_id)
        )

        if not existing_comment:
            raise EntityNotFoundException(
                message=f"Comment with id {comment_id} not found.",
                data={"comment_id": comment_id},
            )

        if existing_comment.is_deleted:
            raise EntityNotFoundException(
                message=f"Comment with id {comment_id} not found or deleted.",
                data={"comment_id": comment_id},
            )

        if existing_comment.author_id != requesting_user_id and not is_superuser:
            raise PermissionDeniedException(
                message="You are not allowed to edit this comment.",
                data={"comment_id": comment_id, "requesting_user_id": requesting_user_id},
            )

        updated_comment: Comment = await self.comment_repository.update_comment_content(
            existing_comment, new_content
        )

        return CommentOut.model_validate(updated_comment)
