from abc import ABC, abstractmethod

from ..models import Comment


class CommentRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, comment: Comment) -> Comment:
        ...

    @abstractmethod
    async def get_by_id(self, comment_id: int) -> Comment | None:
        ...

    @abstractmethod
    async def list_by_post(
            self, post_id: int, skip: int = 0, limit: int = 20
    ) -> tuple[list[Comment], int]:
        ...

    @abstractmethod
    async def update(self, comment: Comment, content: str) -> Comment:
        ...

    @abstractmethod
    async def delete(self, comment: Comment) -> None:
        ...

    @abstractmethod
    async def post_exists(self, post_id: int) -> bool:
        ...

    @abstractmethod
    async def get_comment_depth(self, comment_id: int) -> int:
        ...
