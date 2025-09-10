from app.common.exceptions.app_exceptions import EntityNotFoundException, DatabaseOperationException

from ..models import Comment
from ..repositories import CommentRepositoryInterface
from ..schemas import CommentOut


class GetComment:

    def __init__(self, comment_repository: CommentRepositoryInterface) -> None:
        self.comment_repository = comment_repository

    async def execute(self, *, comment_id: int) -> CommentOut:
        """
        Fetch a comment by ID.

        Args:
            comment_id (int): The ID of the comment to fetch.

        Raises:
            EntityNotFoundException: If the comment does not exist or has been deleted.
                Includes {"comment_id": comment_id} in exception data.
            DatabaseOperationException: If a database operation fails during read.
                Includes {"comment_id": comment_id} in exception data.

        Returns:
            CommentOut: The retrieved comment.
        """

        try:
            existing_comment: Comment | None = await self.comment_repository.get_comment_by_id(comment_id)
        except Exception as e:
            raise DatabaseOperationException(
                operation="read",
                message=f"Failed to fetch comment with id {comment_id}",
                data={"comment_id": comment_id},
            ) from e

        if not existing_comment or existing_comment.is_deleted:
            raise EntityNotFoundException(
                message=f"Comment with id {comment_id} not found or deleted.",
                data={"comment_id": comment_id},
            )

        return CommentOut.model_validate(existing_comment)
