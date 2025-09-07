from app.core.exceptions.app_exceptions import ConflictException, ValidationException

from ..repositories import PostRepositoryInterface
from ..schemas import PostCreate, PostOut
from ..utils import slugify


class CreatePost:
    """
    Use case for creating a new post.

    Business rules:
      - A post must have non-empty title and content.
      - Slug must be unique across all posts.
      - If no slug is provided, it will be generated from the title.
      - Slug and title are normalized before saving.
      - Author ID is always enforced from the authenticated user.

    Args:
        repo (PostRepositoryInterface): Repository abstraction for posts.

    Methods:
        execute(data, author_id):
            Create a new post owned by the given author.
            Returns a PostOut object.
    """

    def __init__(self, repo: PostRepositoryInterface):
        self.repo = repo

    async def execute(self, *, data: PostCreate, author_id: int) -> PostOut:
        create_data = data.model_dump(exclude_unset=True)

        title = (create_data.get("title") or "").strip()
        content = (create_data.get("content") or "").strip()
        slug = (
            (create_data.get("slug") or "").strip() if create_data.get("slug") else None
        )

        if not title:
            raise ValidationException("Title cannot be empty")
        if not content:
            raise ValidationException("Content cannot be empty")

        raw_slug: str = slug if slug is not None else title
        slug = slugify(raw_slug)

        if await self.repo.get_by_slug(slug):
            raise ConflictException(f"Slug '{slug}' is already in use")

        create_data.update(
            title=title,
            content=content,
            slug=slug,
            author_id=author_id,
        )

        new_post = await self.repo.create(**create_data)
        return PostOut.model_validate(new_post)
