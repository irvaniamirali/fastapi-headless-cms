from app.common.exceptions import EntityNotFoundException

from ..repositories import PostRepositoryInterface
from ..schemas import PostOut


class GetPost:

    def __init__(self, post_repository: PostRepositoryInterface) -> None:
        self.post_repository = post_repository

    async def execute(self, *, id_or_slug: str) -> PostOut:
        """
        Retrieve a post by ID or slug.

        Args:
            id_or_slug (str): Post ID (as string) or slug.

        Raises:
            EntityNotFoundException: If the post does not exist.
                Includes {"id_or_slug": id_or_slug} in exception data.

        Returns:
            PostOut: The retrieved post.
        """

        post = None

        try:
            post_id = int(id_or_slug)
            post = await self.post_repository.get_by_id(post_id)
        except ValueError:
            pass

        if not post:
            post = await self.post_repository.get_by_slug(id_or_slug)

        if not post:
            raise EntityNotFoundException(
                message=f"Post with id or slug '{id_or_slug}' not found.",
                data={"id_or_slug": id_or_slug},
            )

        return PostOut.model_validate(post)
