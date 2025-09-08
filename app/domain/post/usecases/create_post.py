from app.common.exceptions import DuplicateEntryException

from ..repositories import PostRepositoryInterface
from ..schemas import PostCreate, PostOut
from ..utils import slugify


class CreatePost:

    def __init__(self, post_repository: PostRepositoryInterface) -> None:
        self.post_repository = post_repository

    async def execute(self, *, data: PostCreate, author_id: int) -> PostOut:
        """
        Create a new post.

        Args:
            data (PostCreate): Input data for the post.
            author_id (int): ID of the author creating the post.

        Raises:
            DuplicateEntryException: If the slug is already in use.
                Includes {"slug": slug} in exception data.

        Returns:
            PostOut: The created post.
        """

        create_data = data.model_dump(exclude_unset=True)
        slug = slugify(create_data["slug"] or create_data["title"])

        if await self.post_repository.get_by_slug(slug):
            raise DuplicateEntryException(
                field="slug", value=slug
            )

        create_data.update(slug=slug, author_id=author_id)
        new_post = await self.post_repository.create(**create_data)
        return PostOut.model_validate(new_post)
