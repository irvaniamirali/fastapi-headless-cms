from app.common.exceptions import (
    EntityNotFoundException,
    PermissionDeniedException,
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
        """

        post = await self.post_repository.get_by_id(post_id)

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

        await self.post_repository.delete(post=post)
        return PostOut.model_validate(post)
