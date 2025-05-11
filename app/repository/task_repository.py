from uuid import UUID
from typing import List

from sqlalchemy import select

from app.database import db
from app.repository.crud_repository import CrudRepository
from app.models.models import Task


class TaskRepository(CrudRepository[Task, UUID]):
    async def find_all_by_user_id(self, user_id: UUID) -> List[Task]:
        stmt = select(Task).where(
            Task.user_id == user_id
        )

        result = await db.session.execute(stmt)
        task_list = result.scalars().all()

        return task_list
