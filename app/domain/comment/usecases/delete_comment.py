from app.common.exceptions import EntityNotFoundException, PermissionDeniedException

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

        Raises:
            EntityNotFoundException: If the comment with the given ID does not exist.
            PermissionDeniedException:
                - If the comment is already deleted.
                - If the requesting user is neither the author nor a superuser.
        """

        existing_comment: Comment | None = (
            await self.comment_repository.get_comment_by_id(comment_id)
        )

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

        await self.comment_repository.soft_delete_comment(existing_comment)
        return CommentOut.model_validate(existing_comment)
