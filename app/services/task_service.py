from typing import List
from uuid import UUID
import logging

from app.crud.task_crud import TaskCrud
from app.schemas.task_schema import CreateTaskSchema, TaskSchema
from app.models.models import Task


class TaskService:
    def __init__(self, task_crud: TaskCrud):
        self._task_crud = task_crud

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
        new_task = await self._task_crud.create_task(
            user_id=user_id,
            task_type_id=task.task_type_id,
            name=task.name,
            priority=task.priority,
            date_start=task.date_start,
            date_end=task.date_end
        )

        return self.__map_task_model_to_schema(task=new_task)

    async def update_task(self) -> TaskSchema:
        pass

    async def get_task(self) -> TaskSchema:
        pass

    async def get_user_task_list(self) -> List[TaskSchema]:
        pass
