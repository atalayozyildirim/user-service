from fastapi import APIRouter
from routers.user.user import router as user_router

router = APIRouter()

router.include_router(user_router, prefix="/api", tags=["user"])