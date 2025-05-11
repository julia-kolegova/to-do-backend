from typing import List, Optional
from uuid import UUID
from datetime import datetime
import logging

from app.repository.task_repository import TaskRepository
from app.schemas.task_schema import CreateTaskSchema, TaskSchema
from app.models.models import Task
from app.models.task_status_enum import TaskStatus
from app.models.task_priority_enum import Priority


class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self._task_repository = task_repository

    @staticmethod
    def __map_task_model_to_schema(task: Task) -> TaskSchema | None:
        promo_dict = task.__dict__
        promo_dict.pop('_sa_instance_state', None)

        try:
            return TaskSchema(**promo_dict)
        except Exception as e:
            logging.error(e)
            return None

    async def create_task(self, user_id: UUID, task: CreateTaskSchema) -> TaskSchema:
        task_model = Task(
            user_id=user_id,
            task_type_id=task.task_type_id,
            name=task.name,
            priority=task.priority,
            created_at=datetime.now(),
            date_start=task.date_start,
            date_end=task.date_end
        )

        new_task = await self._task_repository.save(entity=task_model)
        return self.__map_task_model_to_schema(task=new_task)

    async def update_task(
            self,
            task_id: UUID,
            task_type_id: Optional[UUID] = None,
            name: Optional[str] = None,
            priority: Optional[Priority] = None,
            date_start: Optional[datetime] = None,
            date_end: Optional[datetime] = None,
            status: Optional[TaskStatus] = None
    ) -> TaskSchema:
        data = {}

        if task_type_id is not None:
            data["task_type_id"] = task_type_id
        if name is not None:
            data["name"] = name
        if priority is not None:
            data["priority"] = priority
        if date_start is not None:
            data["date_start"] = date_start
        if date_end is not None:
            data["date_end"] = date_end
        if date_start is not None:
            data["status"] = status

        updated_task = await self._task_repository.update(entity_id=task_id, data=data)
        return self.__map_task_model_to_schema(task=updated_task)

    async def get_user_task_list(
            self,
            user_id: UUID,
            status: TaskStatus,
            task_type_id: Optional[UUID] = None
    ) -> List[TaskSchema]:
        task_list = []
        tasks = await self._task_repository.find_all_by_user_id_and_status_and_task_type_id(
            user_id=user_id,
            status=status,
            task_type_id=task_type_id
        )

        for task in tasks:
            task_list.append(self.__map_task_model_to_schema(task=task))

        return task_list
