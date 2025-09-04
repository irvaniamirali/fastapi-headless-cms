from ..repositories import PostRepositoryInterface
from ..schemas import PostList, PostOut


class ListPosts:
    """
    Use case for listing posts with optional pagination and search.

    This class delegates the actual retrieval logic to the
    `PostRepositoryInterface` implementation and converts the raw
    repository data into the schema objects expected by the API layer.

    Args:
        post_repository (PostRepositoryInterface): Repository abstraction
            for accessing post data.

    Methods:
        execute(skip, limit, search):
            Retrieve a list of posts, optionally filtered by search term,
            with pagination support. Returns a `PostList` object containing
            the total count and the list of `PostOut` items.

    Example:
        list_posts = ListPosts(repo)
        posts = await list_posts.execute(skip=0, limit=10, search="fastapi")
    """

    def __init__(self, post_repository: PostRepositoryInterface):
        self.post_repository = post_repository

    async def execute(
            self,
            *,
            skip: int = 0,
            limit: int = 20,
            search: str | None = None,
    ) -> PostList:
        items, total = await self.post_repository.list(
            skip=skip, limit=limit, search=search
        )
        return PostList(
            total=total,
            items=[PostOut.model_validate(post) for post in items],
        )
