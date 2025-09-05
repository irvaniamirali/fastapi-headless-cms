from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_session

from .repositories import CommentRepositoryInterface, CommentRepository

def get_comment_repository(
        session: Annotated[AsyncSession, Depends(get_session)]
) -> CommentRepositoryInterface:
    return CommentRepository(session=session)
