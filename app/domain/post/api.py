from typing import Annotated

import orjson
from fastapi import APIRouter, Request, Response, Depends, Query, status

from app.common.http_responses import SuccessResponse, SuccessCodes
from app.common.http_responses.success_result import SuccessResult

from app.domain.auth.depends import get_current_authenticated_user
from app.domain.user.schemas import UserRead

from .depends import get_post_repository
from .repositories import PostRepositoryInterface
from .schemas import PostCreate, PostList, PostOut, PostUpdate
from .usecases.create_post import CreatePost
from .usecases.delete_post import DeletePost
from .usecases.get_post import GetPost
from .usecases.list_posts import ListPosts
from .usecases.update_post import UpdatePost

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.post(
    "/",
    response_model=SuccessResponse[PostOut],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new post",
)
async def create_post(
    request: Request,
    data: PostCreate,
    current_user: Annotated[UserRead, Depends(get_current_authenticated_user)],
    post_repository: Annotated[PostRepositoryInterface, Depends(get_post_repository)],
):
    created_post = await CreatePost(post_repository).execute(data=data, author_id=current_user.id)
    result = SuccessResult[PostOut].create(
        code=SuccessCodes.SUCCESS,
        message="Post created successfully",
        status_code=status.HTTP_201_CREATED,
        data=created_post
    )
    return result.to_json_response(request)


@router.get(
    "/",
    response_model=SuccessResponse[PostList],
    summary="List posts with pagination",
    description="Returns a paginated list of posts. Supports optional search by title/content.",
)
async def list_posts(
    request: Request,
    post_repository: Annotated[PostRepositoryInterface, Depends(get_post_repository)],
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(
        20, ge=1, le=100, description="Maximum number of items to return"
    ),
    search: str | None = Query(
        None, min_length=1, description="Search term for title/content"
    ),
):
    posts_list = await ListPosts(post_repository).execute(
        skip=skip,
        limit=limit,
        search=search,
    )
    result = SuccessResult[PostList].create(
        code=SuccessCodes.SUCCESS,
        message="Posts retrieved successfully",
        status_code=status.HTTP_200_OK,
        data=posts_list
    )
    return result.to_json_response(request)


@router.get(
    "/{id_or_slug}",
    response_model=SuccessResponse[PostOut],
    summary="Get a single post",
)
async def get_post(
    request: Request,
    id_or_slug: str,
    post_repository: Annotated[PostRepositoryInterface, Depends(get_post_repository)],
):
    post = await GetPost(post_repository).execute(id_or_slug=id_or_slug)
    result = SuccessResult[PostOut].create(
        code=SuccessCodes.SUCCESS,
        message="Post retrieved successfully",
        status_code=status.HTTP_200_OK,
        data=post
    )
    return result.to_json_response(request)


@router.patch(
    "/{post_id}",
    response_model=SuccessResponse[PostOut],
    summary="Update a post",
)
async def update_post(
    request: Request,
    post_id: int,
    data: PostUpdate,
    current_user: Annotated[UserRead, Depends(get_current_authenticated_user)],
    post_repository: Annotated[PostRepositoryInterface, Depends(get_post_repository)],
):
    updated_post = await UpdatePost(post_repository).execute(
        post_id=post_id,
        data=data,
        actor_id=current_user.id,
        is_superuser=current_user.is_superuser,
    )
    result = SuccessResult[PostOut].create(
        code=SuccessCodes.SUCCESS,
        message="Post updated successfully",
        status_code=status.HTTP_200_OK,
        data=updated_post
    )
    return result.to_json_response(request)



@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a post",
)
async def delete_post(
    response: Response,
    post_id: int,
    current_user: Annotated[UserRead, Depends(get_current_authenticated_user)],
    post_repository: Annotated[PostRepositoryInterface, Depends(get_post_repository)],
):
    deleted_post = await DeletePost(post_repository).execute(
        post_id=post_id,
        actor_id=current_user.id,
        is_superuser=current_user.is_superuser,
    )
    response.headers["X-Deleted-Post"] = orjson.dumps(deleted_post.model_dump()).decode()
    return None
