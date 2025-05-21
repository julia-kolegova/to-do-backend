import os
from dotenv import load_dotenv

if os.path.exists('../.env'):
    load_dotenv('../.env')

import pytest
from uuid import uuid4
from unittest.mock import AsyncMock

from app.services.task_type_service import TaskTypeService
from app.models.models import TaskType
from app.schemas.task_type_schema import TaskTypeResponse


@pytest.fixture
def mock_repository():
    return AsyncMock()


@pytest.fixture
def task_type_service(mock_repository):
    return TaskTypeService(task_type_repository=mock_repository)


@pytest.fixture
def sample_task_type():
    return TaskType(
        id=uuid4(),
        type_name="Work",
        user_id=uuid4()
    )


@pytest.mark.asyncio
async def test_create_task_type_existing(task_type_service, mock_repository, sample_task_type):
    mock_repository.find_by_name_and_user_id.return_value = sample_task_type

    result = await task_type_service.create_task_type(
        user_id=sample_task_type.user_id,
        type_name=sample_task_type.type_name
    )

    assert isinstance(result, TaskTypeResponse)
    assert result.id == sample_task_type.id
    assert result.type_name == sample_task_type.type_name
    mock_repository.find_by_name_and_user_id.assert_called_once()
    mock_repository.save.assert_not_called()


@pytest.mark.asyncio
async def test_create_task_type_new(task_type_service, mock_repository, sample_task_type):
    mock_repository.find_by_name_and_user_id.return_value = None
    mock_repository.save.return_value = sample_task_type

    result = await task_type_service.create_task_type(
        user_id=sample_task_type.user_id,
        type_name=sample_task_type.type_name
    )

    assert isinstance(result, TaskTypeResponse)
    assert result.id == sample_task_type.id
    mock_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_delete_task_type(task_type_service, mock_repository):
    task_type_id = uuid4()

    await task_type_service.delete_task_type(task_type_id=task_type_id)

    mock_repository.delete_by_id.assert_called_once_with(entity_id=task_type_id)


@pytest.mark.asyncio
async def test_find_all_by_user_id(task_type_service, mock_repository, sample_task_type):
    user_id = sample_task_type.user_id
    mock_repository.find_all_by_user_id.return_value = [sample_task_type]

    result = await task_type_service.find_all_by_user_id(user_id=user_id)

    assert isinstance(result, list)
    assert isinstance(result[0], TaskTypeResponse)
    assert result[0].type_name == sample_task_type.type_name
    mock_repository.find_all_by_user_id.assert_called_once_with(user_id=user_id)
