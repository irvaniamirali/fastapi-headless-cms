from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_session

from .repositories import PostRepositoryInterface, PostRepository


def get_post_repository(
        session: Annotated[AsyncSession, Depends(get_session)]
) -> PostRepositoryInterface:
    return PostRepository(session)
