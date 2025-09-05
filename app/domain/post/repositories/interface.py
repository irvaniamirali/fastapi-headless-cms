from abc import ABC, abstractmethod

from ..models import Post


class PostRepositoryInterface(ABC):
    @abstractmethod
    async def get_by_id(self, post_id: int) -> Post | None: ...

    @abstractmethod
    async def get_by_slug(self, slug: str) -> Post | None: ...

    @abstractmethod
    async def list(
        self, *, skip: int = 0, limit: int = 20, search: str | None = None
    ) -> tuple[list[Post], int]: ...

    @abstractmethod
    async def create(
        self,
        *,
        title: str,
        content: str,
        author_id: int,
        slug: str | None = None,
    ) -> Post: ...

    @abstractmethod
    async def update(
        self,
        *,
        post: Post,
        title: str | None = None,
        content: str | None = None,
        slug: str | None = None,
    ) -> Post: ...

    @abstractmethod
    async def delete(self, *, post: Post) -> None: ...
