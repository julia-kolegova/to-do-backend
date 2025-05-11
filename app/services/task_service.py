from typing import List
from uuid import UUID
from datetime import datetime
import logging

from app.repository.task_repository import TaskRepository
from app.schemas.task_schema import CreateTaskSchema, TaskSchema
from app.models.models import Task


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

    async def update_task(self) -> TaskSchema:
        pass

    async def get_task(self) -> TaskSchema:
        pass

    async def get_user_task_list(self, user_id: UUID) -> List[TaskSchema]:
        task_list = []
        tasks = await self._task_repository.find_all_by_user_id(user_id=user_id)

        for task in tasks:
            task_list.append(self.__map_task_model_to_schema(task=task))

        return task_list
