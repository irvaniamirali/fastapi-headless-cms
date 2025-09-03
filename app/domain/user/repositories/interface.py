from abc import ABC, abstractmethod
from typing import Any

from app.domain.user.models import User


class UserRepositoryInterface(ABC):
    @abstractmethod
    async def insert(self, user: User) -> User:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        ...

    @abstractmethod
    async def create(self, *, email: str, hashed_password: str) -> User:
        ...

    @abstractmethod
    async def exists(self, field: str, value: Any) -> bool:
        ...
