from abc import ABC, abstractmethod

from ..models import Post


class PostRepositoryInterface(ABC):
    @abstractmethod
    async def get_post_by_id(self, post_id: int) -> Post | None:
        pass

    @abstractmethod
    async def get_post_by_slug(self, slug: str) -> Post | None:
        pass

    @abstractmethod
    async def post_exists(self, post_id: int) -> bool:
        pass

    @abstractmethod
    async def list_posts(
        self, *, skip: int = 0, limit: int = 20, search: str | None = None
    ) -> tuple[list[Post], int]:
        pass

    @abstractmethod
    async def create_post(
        self, *, title: str, content: str, author_id: int, slug: str | None = None
    ) -> Post:
        pass

    @abstractmethod
    async def update_post(
        self,
        *,
        post: Post,
        title: str | None = None,
        content: str | None = None,
        slug: str | None = None
    ) -> Post:
        pass

    @abstractmethod
    async def delete_post(self, *, post: Post) -> None:
        pass
