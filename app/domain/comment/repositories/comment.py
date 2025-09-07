from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.post.models import Post

from ..models import Comment
from .interface import CommentRepositoryInterface


class CommentRepository(CommentRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, comment: Comment) -> Comment:
        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)
        return comment

    async def get_by_id(self, comment_id: int) -> Comment | None:
        result = await self.session.execute(
            select(Comment)
            .where(Comment.id == comment_id, Comment.is_deleted.is_(False))
            .options(selectinload(Comment.replies))
        )
        return result.scalar_one_or_none()

    async def list_by_post(
        self, post_id: int, skip: int = 0, limit: int = 20
    ) -> tuple[list[Comment], int]:
        query = (
            select(Comment)
            .where(Comment.post_id == post_id, Comment.is_deleted.is_(False))
            .options(selectinload(Comment.replies))
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(query)
        items: list[Comment] = result.scalars().all()  # type: ignore[assignment]

        total_query = (
            select(func.count())
            .select_from(Comment)
            .where(Comment.post_id == post_id, Comment.is_deleted.is_(False))
        )
        total_result = await self.session.execute(total_query)
        total: int = total_result.scalar_one()

        return items, total

    async def update(self, comment: Comment, content: str) -> Comment:
        comment.content = content  # type: ignore[assignment]
        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)
        updated = await self.get_by_id(int(comment.id))
        return updated or comment

    async def delete(self, comment: Comment) -> None:
        """Soft delete a comment."""
        comment.is_deleted = True  # type: ignore[assignment]
        self.session.add(comment)
        await self.session.commit()

    async def post_exists(self, post_id: int) -> bool:
        result = await self.session.execute(select(Post.id).where(Post.id == post_id))
        return result.scalar_one_or_none() is not None

    async def get_comment_depth(self, comment_id: int) -> int:
        """Return the nesting depth of a comment."""
        depth = 0
        current_id = comment_id

        while current_id:
            result = await self.session.execute(
                select(Comment.parent_id).where(Comment.id == current_id)
            )
            parent_id = result.scalar_one_or_none()
            if not parent_id:
                break
            depth += 1
            current_id = parent_id

        return depth
