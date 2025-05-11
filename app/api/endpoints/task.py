from typing import List

from fastapi import APIRouter, Depends

from app.api.jwt import get_jwt_token
from app.schemas.task_schema import TaskSchema, CreateTaskSchema
from app.services.task_service import TaskService
from app.depends import get_task_service

task_router = APIRouter(prefix='/tasks')
task_router.tags = ["Task"]


@task_router.post('/', response_model=TaskSchema)
async def create_task(
        new_task: CreateTaskSchema,
        credentials: dict = Depends(get_jwt_token),
        task_service: TaskService = Depends(get_task_service)
):
    user_id = credentials["id"]

    return await task_service.create_task(user_id=user_id, task=new_task)


# @task_router.patch('/', response_model=AuthUser)
# async def update_task(new_user: CreateUserSchema):
#     pass


@task_router.get('/', response_model=List[TaskSchema])
async def get_task_list(
        credentials: dict = Depends(get_jwt_token),
        task_service: TaskService = Depends(get_task_service)
):
    user_id = credentials["id"]
    return await task_service.get_user_task_list(user_id=user_id)
