from app.core.exceptions.app_exceptions import NotFoundException

from ..repositories import PostRepositoryInterface
from ..schemas import PostOut


class GetPost:
    """
    Use case for retrieving a post by either ID or slug.

    This class attempts to interpret the given identifier (`id_or_slug`) as an
    integer ID first. If conversion fails, it falls back to treating the input
    as a slug. If the post cannot be found by either method, a
    `NotFoundException` is raised.

    Example:
        get_post = GetPost(repo)
        post = await get_post.execute(id_or_slug="42")       # by ID
        post = await get_post.execute(id_or_slug="my-slug")  # by slug
    """

    def __init__(self, post_repository: PostRepositoryInterface):
        self.post_repository = post_repository

    async def execute(self, *, id_or_slug: str) -> PostOut:
        post = None

        try:
            post_id = int(id_or_slug)
            post = await self.post_repository.get_by_id(post_id)
        except ValueError:
            pass

        if not post:
            post = await self.post_repository.get_by_slug(id_or_slug)

        if not post:
            raise NotFoundException("Post not found")

        return PostOut.model_validate(post)
