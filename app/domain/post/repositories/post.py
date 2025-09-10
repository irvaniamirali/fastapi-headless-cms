from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Post
from ..utils import slugify
from .interface import PostRepositoryInterface


class PostRepository(PostRepositoryInterface):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_post_by_id(self, post_id: int) -> Post | None:
        res = await self.session.execute(select(Post).where(Post.id == post_id))
        return res.scalar_one_or_none()

    async def get_post_by_slug(self, slug: str) -> Post | None:
        res = await self.session.execute(select(Post).where(Post.slug == slug))
        return res.scalar_one_or_none()

    async def post_exists(self, post_id: int) -> bool:
        res = await self.session.execute(select(Post.id).where(Post.id == post_id))
        return res.scalar_one_or_none() is not None

    async def list_posts(
        self, *, skip: int = 0, limit: int = 20, search: str | None = None
    ) -> tuple[list[Post], int]:
        stmt = select(Post)
        count_stmt = select(func.count()).select_from(Post)

        if search:
            like = f"%{search.lower()}%"
            stmt = stmt.where(func.lower(Post.title).like(like))
            count_stmt = count_stmt.where(func.lower(Post.title).like(like))

        stmt = stmt.order_by(Post.created_at.desc()).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        items = list(result.scalars().all())

        total_res = await self.session.execute(count_stmt)
        total = int(total_res.scalar() or 0)
        return items, total

    async def create_post(
        self, *, title: str, content: str, author_id: int, slug: str | None = None
    ) -> Post:
        base_slug = slugify(slug or title)
        unique_slug = await self._ensure_unique_slug(base_slug)
        post = Post(title=title, content=content, author_id=author_id, slug=unique_slug)
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)
        return post

    async def update_post(
        self,
        *,
        post: Post,
        title: str | None = None,
        content: str | None = None,
        slug: str | None = None
    ) -> Post:
        if title is not None:
            post.title = title
        if content is not None:
            post.content = content
        if slug is not None:
            base_slug = slugify(slug or post.title)
            post.slug = await self._ensure_unique_slug(base_slug)

        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)
        return post

    async def delete_post(self, *, post: Post) -> None:
        await self.session.delete(post)
        await self.session.commit()

    async def _ensure_unique_slug(self, base_slug: str) -> str:

        if not base_slug:
            base_slug = "post"

        candidate = base_slug
        i = 1
        while True:
            res = await self.session.execute(select(Post.slug).where(Post.slug == candidate))
            if res.scalar_one_or_none() is None:
                return candidate
            i += 1
            candidate = f"{base_slug}-{i}"
