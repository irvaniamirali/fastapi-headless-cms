from app.common.exceptions import (
    EntityNotFoundException,
    PermissionDeniedException,
    ValidationException,
)
from app.domain.post.repositories import PostRepositoryInterface

from ..models import Comment
from ..repositories import CommentRepositoryInterface
from ..schemas import CommentCreate, CommentOut


class CreateComment:

    def __init__(
        self,
        comment_repository: CommentRepositoryInterface,
        post_repository: PostRepositoryInterface,
    ) -> None:
        self.comment_repository = comment_repository
        self.post_repository = post_repository

    async def execute(
        self, *, comment_data: CommentCreate, author_id: int
    ) -> CommentOut:
        """
        Create a comment for the given post.

        Raises:
            ValidationException: If content is empty or nesting depth exceeded.
            EntityNotFoundException: If the post or parent comment does not exist.
            PermissionDeniedException: If parent belongs to another post or is deleted.

        Returns:
            CommentOut: The created comment.
        """

        post_exists = await self.post_repository.post_exists(comment_data.post_id)

        if not post_exists:
            raise EntityNotFoundException(
                message=f"Post with id {comment_data.post_id} was not found.",
                data={"post_id": comment_data.post_id},
            )

        if comment_data.parent_id:
            existing_parent_comment = await self.comment_repository.get_comment_by_id(
                comment_data.parent_id
            )
            if not existing_parent_comment:
                raise EntityNotFoundException(
                    message=f"Parent comment with id {comment_data.parent_id} was not found.",
                    data={"parent_id": comment_data.parent_id},
                )

            if existing_parent_comment.post_id != comment_data.post_id:
                raise PermissionDeniedException(
                    message="Parent comment belongs to a different post",
                    data={
                        "parent_id": existing_parent_comment.post_id,
                        "post_id": comment_data.post_id,
                    }
                )

            if existing_parent_comment.is_deleted:
                raise EntityNotFoundException(
                    message=f"Comment with id {comment_data.parent_id} not found or deleted.",
                    data={"comment_id": comment_data.parent_id},
                )

            parent_comment_depth = (
                await self.comment_repository.get_comment_nesting_depth(
                    comment_data.parent_id
                )
            )
            if parent_comment_depth >= 2:
                raise ValidationException(
                    message="Maximum reply depth reached",
                    data={"parent_id": comment_data.parent_id, "max_depth": 2}
                )

        new_comment_entity = Comment(
            post_id=comment_data.post_id,
            author_id=author_id,
            content=comment_data.content.strip(),
            parent_id=comment_data.parent_id,
        )

        created_comment: Comment = await self.comment_repository.create_comment(
            new_comment_entity
        )

        return CommentOut(
            id=created_comment.id,
            post_id=created_comment.post_id,
            author_id=created_comment.author_id,
            content=created_comment.content,
            parent_id=created_comment.parent_id,
            replies=[],
        )
