from typing import List
from datetime import datetime
from uuid import UUID, uuid4

from fastapi_sqlalchemy import db

from app.crud.db_operations import DBOperations

from app.models.models import Task
from app.models.task_priority_enum import Priority


class TaskCrud(DBOperations):
    @staticmethod
    async def get_task(task_id: UUID) -> Task | None:
        task = db.session.query(Task).filter(Task.id == task_id).first()

        return task

    @staticmethod
    async def get_all_users_task(user_id: UUID) -> List[Task]:
        task_list = db.session.query(Task).filter(Task.user_id == user_id).all()
        return task_list

    async def create_task(
            self,
            user_id: UUID,
            task_type_id: UUID,
            name: str,
            priority: Priority,
            date_start: datetime,
            date_end: datetime
    ) -> Task:
        task = Task(
            id=uuid4(),
            user_id=user_id,
            task_type_id=task_type_id,
            name=name,
            priority=priority,
            created_at=datetime.now(),
            date_start=date_start,
            date_end=date_end
        )

        await self.db_write(task)
        await self.refresh(task)

        return task
