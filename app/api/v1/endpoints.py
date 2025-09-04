from fastapi import APIRouter

from app.domain.auth.api import router as auth_router
from app.domain.post.api import router as post_router
from app.domain.user.api import router as user_router


router = APIRouter(prefix="/v1")

router.include_router(auth_router)
router.include_router(post_router)
router.include_router(user_router)
