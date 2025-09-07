from app.core.exceptions.app_exceptions import (
    NotFoundException,
    PermissionDeniedException,
)

from ..repositories import PostRepositoryInterface


class DeletePost:
    """
    Use case for deleting a post.

    Business rules:
      - The post must exist; otherwise, NotFoundException is raised.
      - Only the post author or a superuser can delete the post;
        otherwise, PermissionDeniedException is raised.
      - Delegates the deletion operation to the repository.

    Args:
        repo (PostRepositoryInterface): Repository abstraction for posts.

    Methods:
        execute(post_id, actor_id, is_superuser):
            Deletes the specified post if the actor has permission.

    Example:
        delete_post = DeletePost(repo)
        await delete_post.execute(
            post_id=1,
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
        actor_id: int,
        is_superuser: bool = False,
    ) -> None:
        post = await self.post_repository.get_by_id(post_id)
        if not post:
            raise NotFoundException("Post not found")

        if post.author_id != actor_id and not is_superuser:
            raise PermissionDeniedException("Not allowed to delete this post")

        await self.post_repository.delete(post=post)
