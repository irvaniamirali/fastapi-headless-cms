from app.core.exceptions.app_exceptions import (
    PermissionDeniedException,
    NotFoundException,
)

from ..repositories import PostRepositoryInterface
from ..schemas import PostUpdate, PostOut


class UpdatePost:
    """
    Use case for updating a post.

    This use case ensures that:
      - The post exists, otherwise raises `NotFoundException`.
      - The actor is either the author of the post or a superuser,
        otherwise raises `PermissionDeniedException`.
      - The repository handles persistence of updated fields.

    Args:
        post_repository (PostRepositoryInterface): Repository abstraction
            for accessing and modifying post data.

    Methods:
        execute(post_id, data, actor_id, is_superuser):
            Update a post with new data, applying ownership rules.
            Returns a `PostOut` object representing the updated post.

    Example:
        update_post = UpdatePost(repo)
        post = await update_post.execute(
            post_id=1,
            data=PostUpdate(title="New title"),
            actor_id=current_user.id,
            is_superuser=current_user.is_superuser,
        )
    """

    def __init__(self, post_repository: PostRepositoryInterface):
        self.post_repository = post_repository

    async def execute(
        self,
        *,
        post_id: int,
        data: PostUpdate,
        actor_id: int,
        is_superuser: bool = False,
    ) -> PostOut:
        post = await self.post_repository.get_by_id(post_id)
        if not post:
            raise NotFoundException("Post not found")

        if post.author_id != actor_id and not is_superuser:
            raise PermissionDeniedException("Not allowed to edit this post")

        update_data = data.model_dump(exclude_unset=True)
        updated = await self.post_repository.update(post=post, **update_data)

        return PostOut.model_validate(updated)
