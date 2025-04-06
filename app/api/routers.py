from fastapi import APIRouter

from app.api.endpoints.user import user_router


api_router = APIRouter(prefix="/v1")
api_router.include_router(user_router)
