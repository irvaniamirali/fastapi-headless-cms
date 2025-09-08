from abc import ABC, abstractmethod
from typing import Any

from app.domain.user.models import User


class UserRepositoryInterface(ABC):
    @abstractmethod
    async def create_user(self, email: str, password: str) -> User:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    async def exists(self, field: str, value: Any) -> bool:
        pass
