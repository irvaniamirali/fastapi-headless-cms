from app.core.exceptions.app_exceptions import NotFoundException

from ..repositories import CommentRepositoryInterface
from ..schemas import CommentOut, CommentList


class ListComments:
    """
    Use case for listing comments of a post.
    Supports pagination and returns both items and total count.
    """

    def __init__(self, comment_repository: CommentRepositoryInterface):
        self.comment_repository = comment_repository

    async def execute(self, *, post_id: int, skip: int = 0, limit: int = 20) -> CommentList:
        """
        List comments for a given post with pagination.

        Args:
            post_id (int): The ID of the post whose comments should be listed.
            skip (int): Number of items to skip (default=0).
            limit (int): Maximum number of items to return (default=20).

        Returns:
            CommentList: A list of comments and the total count.
        """

        post_exists = await self.comment_repository.post_exists(post_id)

        if not post_exists:
            raise NotFoundException("Post not found")

        comments, total = await self.comment_repository.list_by_post(post_id, skip=skip, limit=limit)
        return CommentList(total=total, items=[CommentOut.model_validate(comment) for comment in comments])
