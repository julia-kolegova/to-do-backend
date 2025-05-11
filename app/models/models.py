from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base
from app.models.task_priority_enum import Priority
from app.models.task_status_enum import TaskStatus


class User(Base):
    __tablename__ = "user"

    id = Column(UUID, primary_key=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True, unique=True)
    password = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True, default=datetime.now())


class TaskType(Base):
    __tablename__ = "task_type"

    id = Column(UUID, primary_key=True)
    type_name = Column(String, nullable=False)


class Task(Base):
    __tablename__ = "task"

    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, ForeignKey('user.id', ondelete='CASCADE'))
    task_type_id = Column(UUID, ForeignKey('task_type.id', ondelete='CASCADE'), nullable=True)
    name = Column(String, nullable=False)
    priority = Column(Enum(Priority), nullable=False, default=Priority.NAN)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    date_start = Column(DateTime, nullable=False, default=datetime.now())
    date_end = Column(DateTime, nullable=False, default=datetime.now())
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.ACTIV)
    