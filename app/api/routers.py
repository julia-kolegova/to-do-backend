from fastapi import APIRouter

from app.api.endpoints.user import user_router
from app.api.endpoints.task import task_router
from app.api.endpoints.task_type import task_type_router


api_router = APIRouter(prefix="/v1")
api_router.include_router(user_router)
api_router.include_router(task_router)
api_router.include_router(task_type_router)
