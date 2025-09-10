from app.common.exceptions.app_exceptions import DatabaseOperationException, EntityNotFoundException

from ..repositories import PostRepositoryInterface
from ..schemas import PostList, PostOut


class ListPosts:

    def __init__(self, post_repository: PostRepositoryInterface) -> None:
        self.post_repository = post_repository

    async def execute(
            self,
            *,
            skip: int = 0,
            limit: int = 20,
            search: str | None = None,
    ) -> PostList:
        """
        List posts with pagination and optional search.

        Args:
            skip (int): Number of posts to skip (default=0).
            limit (int): Maximum number of posts to return (default=20).
            search (str | None): Optional search term.

        Raises:
            EntityNotFoundException: If no posts match the criteria.
                Includes {"search": search, "skip": skip, "limit": limit} in exception data.
            DatabaseOperationException: If a database operation fails during read.
                Includes {"search": search, "skip": skip, "limit": limit} in exception data.

        Returns:
            PostList: Object containing total count and list of PostOut items.
        """

        try:
            items, total = await self.post_repository.list_posts(
                skip=skip, limit=limit, search=search
            )
        except Exception as e:
            raise DatabaseOperationException(
                operation="read",
                message="Failed to list posts from database",
                data={"search": search, "skip": skip, "limit": limit},
            ) from e

        return PostList(
            total=total,
            items=[PostOut.model_validate(post) for post in items],
        )
