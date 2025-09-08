from app.common.exceptions import (
    EntityNotFoundException,
    PermissionDeniedException,
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

        Returns:
            PostOut: The updated post.
        """

        post = await self.post_repository.get_by_id(post_id)

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
        updated = await self.post_repository.update(post=post, **update_data)

        return PostOut.model_validate(updated)
