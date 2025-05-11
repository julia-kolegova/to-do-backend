from uuid import UUID
from typing import List, Optional

from sqlalchemy import select

from app.database import db
from app.repository.crud_repository import CrudRepository
from app.models.models import Task
from app.models.task_status_enum import TaskStatus


class TaskRepository(CrudRepository[Task, UUID]):
    async def find_all_by_user_id_and_status_and_task_type_id(
            self,
            user_id: UUID,
            status: TaskStatus,
            task_type_id: Optional[UUID] = None,
    ) -> List[Task]:
        if task_type_id is None:
            stmt = select(Task).where(
                Task.user_id == user_id,
                Task.status == status
            )
        else:
            stmt = select(Task).where(
                Task.user_id == user_id,
                Task.status == status,
                Task.task_type_id == task_type_id
            )

        result = await db.session.execute(stmt)
        task_list = result.scalars().all()

        return task_list
