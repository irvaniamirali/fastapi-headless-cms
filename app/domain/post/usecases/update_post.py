from app.common.exceptions.app_exceptions import (
    EntityNotFoundException,
    PermissionDeniedException,
    DatabaseOperationException
)

from ..repositories import PostRepositoryInterface
from ..schemas import PostOut, PostUpdate


class UpdatePost:

    def __init__(self, post_repository: PostRepositoryInterface) -> None:
        self.post_repository = post_repository

    async def execute(
        self,
        *,
        post_id: int,
        data: PostUpdate,
        actor_id: int,
        is_superuser: bool = False,
    ) -> PostOut:
        """
        Update a post with new data.

        Args:
            post_id (int): ID of the post to update.
            data (PostUpdate): Fields to update.
            actor_id (int): ID of the user performing the update.
            is_superuser (bool): Whether the actor has superuser privileges.

        Raises:
            EntityNotFoundException: If the post does not exist.
                Includes {"post_id": post_id} in exception data.
            PermissionDeniedException: If the actor is neither the author nor a superuser.
                Includes {"post_id": post_id, "actor_id": actor_id} in exception data.
            DatabaseOperationException: If a database operation fails during read or update.
                Includes {"post_id": post_id, "update_data": update_data} in exception data.

        Returns:
            PostOut: The updated post.
        """

        try:
            post = await self.post_repository.get_post_by_id(post_id)
        except Exception as e:
            raise DatabaseOperationException(
                operation="read",
                message=f"Failed to read post with id {post_id}",
                data={"post_id": post_id},
            ) from e

        if not post:
            raise EntityNotFoundException(
                message=f"Post with id {post_id} not found.",
                data={"post_id": post_id},
            )

        if post.author_id != actor_id and not is_superuser:
            raise PermissionDeniedException(
                message="You are not allowed to edit this post.",
                data={"post_id": post_id, "actor_id": actor_id},
            )

        update_data = data.model_dump(exclude_unset=True)

        try:
            updated = await self.post_repository.update_post(post=post, **update_data)
        except Exception as e:
            raise DatabaseOperationException(
                operation="update",
                message=f"Failed to update post with id {post_id}",
                data={"post_id": post_id, "update_data": update_data},
            ) from e

        return PostOut.model_validate(updated)
