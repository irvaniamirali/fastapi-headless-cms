from app.common.exceptions import EntityNotFoundException
from app.domain.post.repositories import PostRepositoryInterface

from ..models import Comment
from ..repositories import CommentRepositoryInterface
from ..schemas import CommentList, CommentOut


class ListComments:

    def __init__(
        self,
        comment_repository: CommentRepositoryInterface,
        post_repository: PostRepositoryInterface,
    ) -> None:
        self.comment_repository = comment_repository
        self.post_repository = post_repository

    async def execute(
        self, *, post_id: int, skip: int = 0, limit: int = 20
    ) -> CommentList:
        """
        List comments for a specific post with pagination.

        Args:
            post_id (int): ID of the post.
            skip (int): Number of comments to skip (default=0).
            limit (int): Maximum number of comments to return (default=20).

        Raises:
            EntityNotFoundException: If the post with the given ID does not exist.
                Includes {"post_id": post_id} in exception data.

        Returns:
            CommentList: Contains total count and list of CommentOut items.
        """

        post_exists: bool = await self.post_repository.post_exists(post_id)

        if not post_exists:
            raise EntityNotFoundException(
                message=f"Post with id {post_id} not found.",
                data={"post_id": post_id},
            )

        comments: list[Comment]
        total_comments_count: int
        comments, total_comments_count = (
            await self.comment_repository.list_comments_by_post_id(
                post_id, skip=skip, limit=limit
            )
        )

        return CommentList(
            total=total_comments_count,
            items=[CommentOut.model_validate(comment) for comment in comments],
        )
