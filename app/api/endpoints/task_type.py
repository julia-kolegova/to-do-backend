from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, status

from app.api.jwt import get_jwt_token
from app.schemas.task_type_schema import TaskTypeResponse
from app.services.task_type_service import TaskTypeService
from app.depends import get_task_type_service

task_type_router = APIRouter(prefix='/task_types')
task_type_router.tags = ["Task type"]


@task_type_router.post('/{type_name}', response_model=TaskTypeResponse)
async def create_task_task_type(
        type_name: str,
        credentials: dict = Depends(get_jwt_token),
        task_type_service: TaskTypeService = Depends(get_task_type_service)
):
    user_id = credentials["id"]

    return await task_type_service.create_task_type(
        user_id=user_id,
        type_name=type_name
    )


@task_type_router.delete('/{task_type_id}')
async def delete_task_task_type(
        task_type_id: UUID,
        credentials: dict = Depends(get_jwt_token),
        task_type_service: TaskTypeService = Depends(get_task_type_service)
):
    await task_type_service.delete_task_type(task_type_id=task_type_id)
    return status.HTTP_204_NO_CONTENT


@task_type_router.get('/', response_model=List[TaskTypeResponse])
async def get_task_type_list(
        credentials: dict = Depends(get_jwt_token),
        task_type_service: TaskTypeService = Depends(get_task_type_service)
):
    user_id = credentials["id"]
    return await task_type_service.find_all_by_user_id(user_id=user_id)
