from app.core.exceptions.app_exceptions import (
    NotFoundException,
    PermissionDeniedException,
    ConflictException,
    ValidationException,
)

from ..repositories import CommentRepositoryInterface
from ..schemas import CommentCreate, CommentOut
from ..models import Comment


class CreateComment:
    """
    Use case for creating a new comment.

    Validates input data, ensures the post exists, checks parent comment
    constraints (same post, not deleted, depth limit), and persists the comment.
    """

    def __init__(self, comment_repository: CommentRepositoryInterface):
        self.comment_repository = comment_repository

    async def execute(self, *, data: CommentCreate, author_id: int) -> CommentOut:
        """
        Create a new comment for a given post.

        Args:
            data (CommentCreate): Input data for the new comment.
            author_id (int): ID of the author creating the comment.

        Raises:
            ValidationException: If content is empty or depth exceeded.
            NotFoundException: If the post or parent comment does not exist.
            PermissionDeniedException: If parent belongs to another post.
            ConflictException: If replying to a deleted parent comment.

        Returns:
            CommentOut: The created comment as an output schema.
        """

        post_exists = await self.comment_repository.post_exists(data.post_id)

        if not post_exists:
            raise NotFoundException("Post not found")

        if data.parent_id:
            parent_comment = await self.comment_repository.get_by_id(data.parent_id)
            if not parent_comment:
                raise NotFoundException("Parent comment not found")

            if parent_comment.post_id != data.post_id:
                raise PermissionDeniedException(
                    "Parent comment belongs to a different post"
                )

            if parent_comment.is_deleted:
                raise ConflictException("Cannot reply to a deleted comment")

            depth = await self.comment_repository.get_comment_depth(data.parent_id)
            if depth >= 2:
                raise ValidationException("Maximum reply depth reached")

        new_comment = Comment(
            post_id=data.post_id,
            author_id=author_id,
            content=data.content.strip(),
            parent_id=data.parent_id,
        )

        created = await self.comment_repository.create(new_comment)

        return CommentOut(
            id=created.id,
            post_id=created.post_id,
            author_id=created.author_id,
            content=created.content,
            parent_id=created.parent_id,
            replies=[]
        )
