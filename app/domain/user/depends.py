from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_session

from .models import User
from .repositories import UserRepository, UserRepositoryInterface


async def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserRepositoryInterface:
    return UserRepository(session, User)
