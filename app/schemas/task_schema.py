from datetime import datetime
from uuid import UUID
from typing import Optional

from pydantic import BaseModel

from app.models.task_priority_enum import Priority
from app.models.task_status_enum import TaskStatus


class CreateTaskSchema(BaseModel):
    task_type_id: Optional[UUID] = None
    name: str
    priority: Priority
    date_start: datetime
    date_end: datetime


class TaskSchema(BaseModel):
    id: UUID
    user_id: UUID
    task_type_id: Optional[UUID] = None
    name: str
    priority: Priority
    created_at: datetime
    date_start: datetime
    date_end: datetime
    status: TaskStatus


class UpdateTaskRequest(BaseModel):
    task_type_id: Optional[UUID] = None
    name: Optional[str] = None
    priority: Optional[Priority] = None
    date_start: Optional[datetime] = None
    date_end: Optional[datetime] = None
