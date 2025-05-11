from uuid import UUID
from typing import List

from app.models.models import TaskType
from app.repository.task_type_repository import TaskTypeRepository
from app.schemas.task_type_schema import TaskTypeResponse


class TaskTypeService:
    def __init__(
            self,
            task_type_repository: TaskTypeRepository
    ):
        self._task_type_repository = task_type_repository

    def __task_type_model_to_schema(self, task_type: TaskType) -> TaskTypeResponse:
        return TaskTypeResponse(
            id=task_type.id,
            type_name=task_type.type_name
        )

    async def create_task_type(self, user_id: UUID, type_name: str) -> TaskTypeResponse:
        task_type = await self._task_type_repository.find_by_name_and_user_id(
            user_id=user_id,
            type_name=type_name
        )

        if task_type is not None:
            return self.__task_type_model_to_schema(task_type)

        task_type_model = TaskType(
            type_name=type_name,
            user_id=user_id
        )
        task_type = await self._task_type_repository.save(task_type_model)
        return self.__task_type_model_to_schema(task_type)

    async def delete_task_type(self, task_type_id: UUID):
        await self._task_type_repository.delete_by_id(entity_id=task_type_id)

    async def find_all_by_user_id(self, user_id: UUID) -> List[TaskTypeResponse]:
        task_type_list = []

        task_types = await self._task_type_repository.find_all_by_user_id(
            user_id=user_id
        )

        for task_type in task_types:
            task_type_list.append(
                self.__task_type_model_to_schema(task_type=task_type)
            )
        return task_type_list
