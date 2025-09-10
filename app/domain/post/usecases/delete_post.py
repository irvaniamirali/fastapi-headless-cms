from app.common.exceptions.app_exceptions import (
    EntityNotFoundException,
    PermissionDeniedException,
    DatabaseOperationException,
)

from ..schemas import PostOut
from ..repositories import PostRepositoryInterface


class DeletePost:

    def __init__(self, post_repository: PostRepositoryInterface) -> None:
        self.post_repository = post_repository

    async def execute(
        self,
        *,
        post_id: int,
        actor_id: int,
        is_superuser: bool = False,
    ) -> PostOut:
        """
        Delete a post by ID.

        Args:
            post_id (int): ID of the post to delete.
            actor_id (int): ID of the user attempting the deletion.
            is_superuser (bool): Whether the actor has superuser privileges.

        Raises:
            EntityNotFoundException: If the post does not exist.
                Includes {"post_id": post_id} in exception data.
            PermissionDeniedException: If the actor is neither the author nor a superuser.
                Includes {"post_id": post_id, "actor_id": actor_id} in exception data.
            DatabaseOperationException: If a database operation fails during read or delete.
                Includes {"post_id": post_id} in exception data.
        """

        try:
            post = await self.post_repository.get_post_by_id(post_id)
        except Exception as e:
            raise DatabaseOperationException(
                operation="read",
                message=f"Failed to get post with id {post_id}",
                data={"post_id": post_id},
            ) from e

        if not post:
            raise EntityNotFoundException(
                message=f"Post with id {post_id} not found.",
                data={"post_id": post_id},
            )

        if post.author_id != actor_id and not is_superuser:
            raise PermissionDeniedException(
                message="You are not allowed to delete this post.",
                data={"post_id": post_id, "actor_id": actor_id},
            )

        try:
            await self.post_repository.delete_post(post=post)
        except Exception as e:
            raise DatabaseOperationException(
                operation="delete",
                message=f"Failed to delete post with id {post_id}",
                data={"post_id": post_id},
            ) from e

        return PostOut.model_validate(post)
