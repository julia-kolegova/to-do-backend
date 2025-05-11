from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.api.jwt import get_jwt_token
from app.schemas.task_schema import (
    TaskSchema,
    CreateTaskSchema,
    UpdateTaskRequest
)
from app.services.task_service import TaskService
from app.models.task_status_enum import TaskStatus
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


@task_router.delete('/{task_id}')
async def delete_task(
        task_id: UUID,
        credentials: dict = Depends(get_jwt_token),
        task_service: TaskService = Depends(get_task_service)
):
    await task_service.update_task(task_id=task_id, status=TaskStatus.DELETED)
    return status.HTTP_204_NO_CONTENT


@task_router.patch('/{task_id}', response_model=TaskSchema)
async def update_task(
        task_id: UUID,
        updated_data: UpdateTaskRequest,
        credentials: dict = Depends(get_jwt_token),
        task_service: TaskService = Depends(get_task_service)
):
    return await task_service.update_task(
        task_id=task_id,
        task_type_id=updated_data.task_type_id,
        name=updated_data.name,
        priority=updated_data.priority,
        date_start=updated_data.date_start,
        date_end=updated_data.date_end
    )


@task_router.get('/{status}', response_model=List[TaskSchema])
async def get_task_list(
        status: TaskStatus,
        task_type_id: Optional[UUID] = None,
        credentials: dict = Depends(get_jwt_token),
        task_service: TaskService = Depends(get_task_service)
):
    user_id = credentials["id"]
    return await task_service.get_user_task_list(
        user_id=user_id,
        status=status,
        task_type_id=task_type_id
    )
