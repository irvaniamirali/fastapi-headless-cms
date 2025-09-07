from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

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
    response_model=PostOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new post",
)
async def create_post(
    data: PostCreate,
    current_user: Annotated[UserRead, Depends(get_current_authenticated_user)],
    post_repository: Annotated[PostRepositoryInterface, Depends(get_post_repository)],
):
    return await CreatePost(post_repository).execute(
        data=data,
        author_id=current_user.id,
    )


@router.get(
    "/",
    response_model=PostList,
    summary="List posts with pagination",
    description="Returns a paginated list of posts. Supports optional search by title/content.",
)
async def list_posts(
    post_repository: Annotated[PostRepositoryInterface, Depends(get_post_repository)],
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(
        20, ge=1, le=100, description="Maximum number of items to return"
    ),
    search: str | None = Query(
        None, min_length=1, description="Search term for title/content"
    ),
):
    """
    List posts with pagination and optional search.

    Returns:
        PostList: Contains total count and list of posts.

    Example:
        GET /posts?skip=0&limit=10&search=fastapi
    """
    return await ListPosts(post_repository).execute(
        skip=skip,
        limit=limit,
        search=search,
    )


@router.get(
    "/{id_or_slug}",
    response_model=PostOut,
    summary="Get a single post",
)
async def get_post(
    id_or_slug: str,
    post_repository: Annotated[PostRepositoryInterface, Depends(get_post_repository)],
):
    """
    Retrieve a single post by its ID (integer) or slug (string).
    """
    return await GetPost(post_repository).execute(id_or_slug=id_or_slug)


@router.patch(
    "/{post_id}",
    response_model=PostOut,
    summary="Update a post",
)
async def update_post(
    post_id: int,
    data: PostUpdate,
    current_user: Annotated[UserRead, Depends(get_current_authenticated_user)],
    post_repository: Annotated[PostRepositoryInterface, Depends(get_post_repository)],
):
    return await UpdatePost(post_repository).execute(
        post_id=post_id,
        data=data,
        actor_id=current_user.id,
        is_superuser=current_user.is_superuser,
    )


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a post",
)
async def delete_post(
    post_id: int,
    current_user: Annotated[UserRead, Depends(get_current_authenticated_user)],
    post_repository: Annotated[PostRepositoryInterface, Depends(get_post_repository)],
):
    await DeletePost(post_repository).execute(
        post_id=post_id,
        actor_id=current_user.id,
        is_superuser=current_user.is_superuser,
    )
    return None
