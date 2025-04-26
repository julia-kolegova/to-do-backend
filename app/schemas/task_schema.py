from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional

from pydantic import BaseModel

from app.models.task_priority_enum import Priority


class CreateTaskSchema(BaseModel):
    task_type_id: Optional[UUID] = None
    name: str
    priority: Priority
    date_start: datetime
    date_end: datetime
    solved: bool = False


class TaskSchema(BaseModel):
    id: UUID
    user_id: UUID
    task_type_id: Optional[UUID] = None
    name: str
    priority: Priority
    created_at: datetime
    date_start: datetime
    date_end: datetime
    solved: bool = False
