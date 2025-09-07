from abc import ABC, abstractmethod

from ..models import Comment


class CommentRepositoryInterface(ABC):
    @abstractmethod
    async def create_comment(self, comment: Comment) -> Comment:
        pass

    @abstractmethod
    async def get_comment_by_id(self, comment_id: int) -> Comment | None:
        pass

    async def list_comments_by_post_id(
        self, post_id: int, skip: int = 0, limit: int = 20
    ) -> tuple[list[Comment], int]:
        pass

    @abstractmethod
    async def update_comment_content(
        self, comment: Comment, new_content: str
    ) -> Comment:
        pass

    @abstractmethod
    async def soft_delete_comment(self, comment: Comment) -> None:
        pass

    @abstractmethod
    async def get_comment_nesting_depth(self, comment_id: int) -> int:
        pass
