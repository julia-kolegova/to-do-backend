from uuid import UUID
from typing import List

from sqlalchemy import select

from app.database import db
from app.repository.crud_repository import CrudRepository
from app.models.models import TaskType


class TaskTypeRepository(CrudRepository[TaskType, UUID]):
    pass
