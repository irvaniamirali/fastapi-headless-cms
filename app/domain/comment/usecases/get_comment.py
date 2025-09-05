from app.core.exceptions.app_exceptions import NotFoundException

from ..repositories import CommentRepositoryInterface
from ..schemas import CommentOut


class GetComment:
    """
    Use case for retrieving a single comment by its ID.
    Ensures the comment exists and is not deleted.
    """

    def __init__(self, comment_repository: CommentRepositoryInterface):
        self.comment_repository = comment_repository

    async def execute(self, *, comment_id: int) -> CommentOut:
        """
        Fetch a comment by ID.

        Args:
            comment_id (int): The ID of the comment to fetch.

        Raises:
            NotFoundException: If the comment does not exist or is deleted.

        Returns:
            CommentOut: The retrieved comment as an output schema.
        """

        comment = await self.comment_repository.get_by_id(comment_id)

        if not comment or comment.is_deleted:
            raise NotFoundException("Comment not found")
        return CommentOut.model_validate(comment)
