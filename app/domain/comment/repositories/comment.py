from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models import Comment
from .interface import CommentRepositoryInterface


class CommentRepository(CommentRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def create_comment(self, comment: Comment) -> Comment:
        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)
        return comment

    async def get_comment_by_id(self, comment_id: int) -> Comment | None:
        execution_result = await self.session.execute(
            select(Comment)
            .where(Comment.id == comment_id, Comment.is_deleted.is_(False))
            .options(selectinload(Comment.replies))
        )
        return execution_result.scalar_one_or_none()

    async def list_comments_by_post_id(
        self, post_id: int, skip: int = 0, limit: int = 20
    ) -> tuple[list[Comment], int]:
        query = (
            select(Comment)
            .where(Comment.post_id == post_id, Comment.is_deleted.is_(False))
            .options(selectinload(Comment.replies))
            .offset(skip)
            .limit(limit)
        )
        execution_result = await self.session.execute(query)
        comments: list[Comment] = execution_result.scalars().all()  # type: ignore[assignment]

        total_query = (
            select(func.count())
            .select_from(Comment)
            .where(Comment.post_id == post_id, Comment.is_deleted.is_(False))
        )
        total_execution_result = await self.session.execute(total_query)
        total_comments_count: int = total_execution_result.scalar_one()

        return comments, total_comments_count

    async def update_comment_content(
        self, comment: Comment, new_content: str
    ) -> Comment:
        comment.content = new_content  # type: ignore[assignment]
        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)
        updated_comment: Comment | None = await self.get_comment_by_id(int(comment.id))
        return updated_comment or comment

    async def soft_delete_comment(self, comment: Comment) -> None:
        """Soft delete a comment."""
        comment.is_deleted = True  # type: ignore[assignment]
        self.session.add(comment)
        await self.session.commit()

    async def get_comment_nesting_depth(self, comment_id: int) -> int:
        """Return the nesting depth of a comment."""
        depth: int = 0
        current_comment_id: int | None = comment_id

        while current_comment_id:
            execution_result = await self.session.execute(
                select(Comment.parent_id).where(Comment.id == current_comment_id)
            )
            parent_comment_id: int | None = execution_result.scalar_one_or_none()
            if not parent_comment_id:
                break
            depth += 1
            current_comment_id = parent_comment_id

        return depth
