from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.jwt import get_jwt_token
from app.schemas.task_schema import TaskSchema, CreateTaskSchema
from app.depends import get_task_service

task_service = get_task_service()

task_type_router = APIRouter(prefix='/task_types')
task_type_router.tags = ["Task type"]


# @task_type_router.post('/{type_name}', response_model=TaskSchema)
# async def create_task_task_type(
#         type_name: str,
#         credentials: dict = Depends(get_jwt_token)
# ):
#     user_id = credentials["id"]
#
#     return await task_service.create_task(user_id=user_id, task=new_task)
#
#
# @task_type_router.delete('/{task_type_id}', response_model=TaskSchema)
# async def delete_task_task_type(
#         task_type_id: UUID,
#         credentials: dict = Depends(get_jwt_token)
# ):
#     user_id = credentials["id"]
#
#     return await task_service.create_task(user_id=user_id, task=new_task)
#
#
# @task_type_router.get('/')
# async def get_task_type(
#         credentials: dict = Depends(get_jwt_token)
# ):
#     user_id = credentials["id"]
#