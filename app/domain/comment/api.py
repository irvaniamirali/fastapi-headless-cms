from typing import Annotated

import orjson
from fastapi import APIRouter, Request, Response, Depends, Path, Query, status

from app.common.http_responses import SuccessResponse, SuccessCodes
from app.common.http_responses.success_result import SuccessResult

from app.domain.auth.depends import get_current_authenticated_user
from app.domain.post.depends import get_post_repository
from app.domain.post.repositories import PostRepositoryInterface
from app.domain.user.schemas import UserRead

from .depends import get_comment_repository
from .repositories import CommentRepositoryInterface
from .schemas import CommentCreate, CommentList, CommentOut, CommentUpdate
from .usecases.create_comment import CreateComment
from .usecases.delete_comment import DeleteComment
from .usecases.list_comments import ListComments
from .usecases.update_comment import UpdateComment

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post(
    "/",
    response_model=SuccessResponse[CommentOut],
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
    request: Request,
    comment_schema: CommentCreate,
    current_user: Annotated[UserRead, Depends(get_current_authenticated_user)],
    comment_repository: Annotated[
        CommentRepositoryInterface, Depends(get_comment_repository)
    ],
    post_repository: Annotated[PostRepositoryInterface, Depends(get_post_repository)],
):
    created_comment = await CreateComment(comment_repository, post_repository).execute(
        comment_data=comment_schema, author_id=current_user.id
    )
    result = SuccessResult[CommentOut].create(
        code=SuccessCodes.SUCCESS,
        message="Comment created successfully",
        status_code=status.HTTP_201_CREATED,
        data=created_comment
    )
    return result.to_json_response(request)


@router.get(
    "/post/{post_id}",
    status_code=status.HTTP_200_OK,
    response_model=SuccessResponse[CommentList],
    summary="List comments for a post",
    responses={
        200: {"description": "List of comments retrieved successfully"},
        404: {"description": "Post not found"},
    },
)
async def list_comments(
    request: Request,
    comment_repository: Annotated[
        CommentRepositoryInterface, Depends(get_comment_repository)
    ],
    post_repository: Annotated[PostRepositoryInterface, Depends(get_post_repository)],
    post_id: Annotated[int, Path(..., ge=1, description="ID of the post")],
    skip: Annotated[
        int, Query(ge=0, description="Number of comments to skip for pagination")
    ] = 0,
    limit: Annotated[
        int, Query(ge=1, le=100, description="Maximum number of comments to return")
    ] = 20,
):
    comments_list = await ListComments(comment_repository, post_repository).execute(
        post_id=post_id, skip=skip, limit=limit
    )
    result = SuccessResult[CommentList].create(
        code=SuccessCodes.SUCCESS,
        message="Comments retrieved successfully",
        status_code=status.HTTP_200_OK,
        data=comments_list
    )
    return result.to_json_response(request)


@router.patch(
    "/{comment_id}",
    status_code=status.HTTP_200_OK,
    response_model=SuccessResponse[CommentOut],
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
    request: Request,
    comment_schema: CommentUpdate,
    comment_id: Annotated[
        int, Path(..., ge=1, description="ID of the comment to update")
    ],
    current_user: Annotated[UserRead, Depends(get_current_authenticated_user)],
    comment_repository: Annotated[
        CommentRepositoryInterface, Depends(get_comment_repository)
    ],
):
    updated_comment = await UpdateComment(comment_repository).execute(
        comment_id=comment_id,
        new_content=comment_schema.content,
        requesting_user_id=current_user.id,
        is_superuser=current_user.is_superuser,
    )
    result = SuccessResult[CommentOut].create(
        code=SuccessCodes.SUCCESS,
        message="Comment updated successfully",
        status_code=status.HTTP_200_OK,
        data=updated_comment
    )
    return result.to_json_response(request)


@router.delete(
    "/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a comment",
    responses={
        204: {"description": "Comment successfully deleted"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden - not allowed to delete this comment"},
        404: {"description": "Comment not found"},
    },
)
async def delete_comment(
    response: Response,
    comment_id: Annotated[
        int, Path(..., ge=1, description="ID of the comment to delete")
    ],
    current_user: Annotated[UserRead, Depends(get_current_authenticated_user)],
    comment_repository: Annotated[
        CommentRepositoryInterface, Depends(get_comment_repository)
    ],
):
    deleted_comment = await DeleteComment(comment_repository).execute(
        comment_id=comment_id,
        requesting_user_id=current_user.id,
        is_superuser=current_user.is_superuser,
    )
    response.headers["X-Deleted-Comment"] = orjson.dumps(deleted_comment.model_dump()).decode()
    return None
