from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status

from app.domain.auth.depends import get_current_authenticated_user
from app.domain.user.schemas import UserRead

from .repositories import CommentRepositoryInterface
from .depends import get_comment_repository
from .schemas import CommentCreate, CommentUpdate, CommentOut, CommentList
from .usecases.create_comment import CreateComment
from .usecases.update_comment import UpdateComment
from .usecases.delete_comment import DeleteComment
from .usecases.list_comments import ListComments

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post(
    "/",
    response_model=CommentOut,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new comment",
    responses={
        201: {"description": "Comment successfully created"},
        401: {"description": "Unauthorized - user must be logged in"},
        404: {"description": "Post not found"},
        422: {"description": "Validation error"},
    },
)
async def create_comment(
    comment_schema: CommentCreate,
    current_user: Annotated[UserRead, Depends(get_current_authenticated_user)],
    comment_repository: CommentRepositoryInterface = Depends(get_comment_repository),
):
    return await CreateComment(comment_repository).execute(
        data=comment_schema, author_id=current_user.id
    )


@router.get(
    "/post/{post_id}",
    status_code=status.HTTP_200_OK,
    response_model=CommentList,
    response_model_exclude_none=True,
    summary="List comments for a post",
    responses={
        200: {"description": "List of comments retrieved successfully"},
        404: {"description": "Post not found"},
    },
)
async def list_comments(
    comment_repository: Annotated[
        CommentRepositoryInterface, Depends(get_comment_repository)
    ],
    post_id: Annotated[int, Path(..., ge=1, description="ID of the post")],
    skip: Annotated[
        int, Query(ge=0, description="Number of comments to skip for pagination")
    ] = 0,
    limit: Annotated[
        int, Query(ge=1, le=100, description="Maximum number of comments to return")
    ] = 20,
):
    return await ListComments(comment_repository).execute(
        post_id=post_id, skip=skip, limit=limit
    )


@router.patch(
    "/{comment_id}",
    status_code=status.HTTP_200_OK,
    response_model=CommentOut,
    response_model_exclude_none=True,
    summary="Update a comment",
    responses={
        200: {"description": "Comment successfully updated"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden - not allowed to update this comment"},
        404: {"description": "Comment not found"},
        422: {"description": "Validation error"},
    },
)
async def update_comment(
    comment_schema: CommentUpdate,
    comment_id: Annotated[
        int, Path(..., ge=1, description="ID of the comment to update")
    ],
    current_user: Annotated[UserRead, Depends(get_current_authenticated_user)],
    comment_repository: Annotated[
        CommentRepositoryInterface, Depends(get_comment_repository)
    ],
):
    return await UpdateComment(comment_repository).execute(
        comment_id=comment_id,
        content=comment_schema.content,
        actor_id=current_user.id,
        is_superuser=current_user.is_superuser,
    )


@router.delete(
    "/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model_exclude_none=True,
    summary="Delete a comment",
    responses={
        204: {"description": "Comment successfully deleted"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden - not allowed to delete this comment"},
        404: {"description": "Comment not found"},
    },
)
async def delete_comment(
    comment_id: Annotated[
        int, Path(..., ge=1, description="ID of the comment to delete")
    ],
    current_user: Annotated[UserRead, Depends(get_current_authenticated_user)],
    comment_repository: Annotated[
        CommentRepositoryInterface, Depends(get_comment_repository)
    ],
):
    await DeleteComment(comment_repository).execute(
        comment_id=comment_id,
        actor_id=current_user.id,
        is_superuser=current_user.is_superuser,
    )
    return None
