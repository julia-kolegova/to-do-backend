from uuid import UUID
from typing import List

from sqlalchemy import select

from app.database import db
from app.repository.crud_repository import CrudRepository
from app.models.models import TaskType


class TaskTypeRepository(CrudRepository[TaskType, UUID]):
    async def find_by_name_and_user_id(
            self,
            type_name: str,
            user_id: UUID
    ) -> TaskType:
        stmt = select(TaskType).where(
            TaskType.type_name == type_name,
            TaskType.user_id == user_id
        )

        result = await db.session.execute(stmt)
        return result.scalars().first()

    async def find_all_by_user_id(
            self,
            user_id: UUID
    ) -> List[TaskType]:
        stmt = select(TaskType).where(
            TaskType.user_id == user_id
        )

        result = await db.session.execute(stmt)
        return result.scalars().all()
