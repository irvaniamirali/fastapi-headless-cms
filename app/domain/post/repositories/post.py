from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from .interface import PostRepositoryInterface
from ..models import Post
from ..utils import slugify


class PostRepository(PostRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, post_id: int) -> Post | None:
        res = await self.session.execute(select(Post).where(Post.id == post_id))
        return res.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Post | None:
        res = await self.session.execute(select(Post).where(Post.slug == slug))
        return res.scalar_one_or_none()

    async def list(
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
        items = result.scalars().all()

        total_res = await self.session.execute(count_stmt)
        total = int(total_res.scalar() or 0)
        return items, total

    async def _ensure_unique_slug(self, base: str) -> str:
        if not base:
            base = "post"
        candidate = base
        i = 1
        while True:
            res = await self.session.execute(
                select(Post.slug).where(Post.slug == candidate)
            )
            if res.scalar_one_or_none() is None:
                return candidate
            i += 1
            candidate = f"{base}-{i}"

    async def create(
        self,
        *,
        title: str,
        content: str,
        author_id: int,
        slug: str | None = None,
    ) -> Post:
        base_slug = slugify(slug or title)
        unique_slug = await self._ensure_unique_slug(base_slug)
        obj = Post(title=title, content=content, author_id=author_id, slug=unique_slug)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(
        self,
        *,
        post: Post,
        title: str | None = None,
        content: str | None = None,
        slug: str | None = None,
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

    async def delete(self, *, post: Post) -> None:
        await self.session.delete(post)
        await self.session.commit()
