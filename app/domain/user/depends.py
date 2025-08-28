from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_db_session

from .repositories import UserRepository


def get_user_repository(db_session: Annotated[AsyncSession, Depends(get_db_session)]) -> UserRepository:
    return UserRepository(db_session)
