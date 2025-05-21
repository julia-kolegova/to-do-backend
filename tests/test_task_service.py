import os
from dotenv import load_dotenv

if os.path.exists('../.env'):
    load_dotenv('../.env')

import pytest
from uuid import uuid4
from datetime import datetime, timedelta
from unittest.mock import AsyncMock

from app.services.task_service import TaskService
from app.schemas.task_schema import CreateTaskSchema, TaskSchema
from app.models.models import Task
from app.models.task_status_enum import TaskStatus
from app.models.task_priority_enum import Priority


@pytest.fixture
def mock_repository():
    return AsyncMock()


@pytest.fixture
def task_service(mock_repository):
    return TaskService(task_repository=mock_repository)


@pytest.fixture
def sample_task():
    return Task(
        id=uuid4(),
        user_id=uuid4(),
        task_type_id=uuid4(),
        name="Test Task",
        priority=Priority.MEDIUM,
        created_at=datetime.now(),
        date_start=datetime.now(),
        date_end=datetime.now() + timedelta(days=1),
        status=TaskStatus.ACTIV
    )


@pytest.mark.asyncio
async def test_create_task(task_service, mock_repository, sample_task):
    create_schema = CreateTaskSchema(
        task_type_id=sample_task.task_type_id,
        name=sample_task.name,
        priority=sample_task.priority,
        date_start=sample_task.date_start,
        date_end=sample_task.date_end
    )
    mock_repository.save.return_value = sample_task

    result = await task_service.create_task(user_id=sample_task.user_id, task=create_schema)

    assert isinstance(result, TaskSchema)
    assert result.name == sample_task.name
    mock_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_update_task(task_service, mock_repository, sample_task):
    mock_repository.update.return_value = sample_task

    result = await task_service.update_task(
        task_id=sample_task.id,
        name="Updated Name"
    )

    assert isinstance(result, TaskSchema)
    assert result.name == sample_task.name
    mock_repository.update.assert_called_once()
    called_data = mock_repository.update.call_args[1]["data"]
    assert called_data["name"] == "Updated Name"


@pytest.mark.asyncio
async def test_get_user_task_list(task_service, mock_repository, sample_task):
    mock_repository.find_all_by_user_id_and_status_and_task_type_id.return_value = [sample_task]

    result = await task_service.get_user_task_list(
        user_id=sample_task.user_id,
        status=TaskStatus.ACTIV
    )

    assert isinstance(result, list)
    assert isinstance(result[0], TaskSchema)
    assert result[0].user_id == sample_task.user_id
    mock_repository.find_all_by_user_id_and_status_and_task_type_id.assert_called_once()
