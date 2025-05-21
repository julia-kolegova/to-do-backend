import os
from dotenv import load_dotenv

if os.path.exists('../.env'):
    load_dotenv('../.env')

import pytest
from uuid import uuid4
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from fastapi.exceptions import HTTPException

from app.services.user_service import UserService
from app.models.models import User
from app.schemas.user_schema import UserSchema


@pytest.fixture
def mock_repository():
    return AsyncMock()


@pytest.fixture
def mock_password_service():
    service = MagicMock()
    service.hash_password.side_effect = lambda password: f"hashed_{password}"
    return service


@pytest.fixture
def user_service(mock_repository, mock_password_service):
    return UserService(password_service=mock_password_service, user_repository=mock_repository)


@pytest.fixture
def sample_user():
    return User(
        id=uuid4(),
        name="Test User",
        email="test@example.com",
        password="hashed_secret",
        created_at=datetime.now()
    )


@pytest.mark.asyncio
async def test_create_user_success(user_service, mock_repository, sample_user):
    mock_repository.find_by_email.return_value = None
    mock_repository.save.return_value = sample_user

    result = await user_service.create_user(
        name="Test User",
        email="test@example.com",
        password="secret",
        confirm_password="secret"
    )

    assert isinstance(result, UserSchema)
    assert result.email == "test@example.com"


@pytest.mark.asyncio
async def test_create_user_password_mismatch(user_service):
    with pytest.raises(HTTPException) as e:
        await user_service.create_user(
            name="Test",
            email="test@example.com",
            password="secret1",
            confirm_password="secret2"
        )
    assert e.value.detail == "Password don`t match"


@pytest.mark.asyncio
async def test_create_user_already_exists(user_service, mock_repository, sample_user):
    mock_repository.find_by_email.return_value = sample_user

    with pytest.raises(HTTPException) as e:
        await user_service.create_user(
            name="Test",
            email="test@example.com",
            password="secret",
            confirm_password="secret"
        )
    assert e.value.detail == "User already exists"


@pytest.mark.asyncio
async def test_get_user_success(user_service, mock_repository, sample_user):
    mock_repository.find_by_id.return_value = sample_user

    result = await user_service.get_user(user_id=sample_user.id)

    assert isinstance(result, UserSchema)
    assert result.id == sample_user.id


@pytest.mark.asyncio
async def test_login_user_success(user_service, mock_repository, sample_user):
    mock_repository.find_by_email.return_value = sample_user

    result = await user_service.login_user(email="test@example.com", password="secret")

    assert isinstance(result, UserSchema)
    assert result.email == "test@example.com"


@pytest.mark.asyncio
async def test_login_user_wrong_password(user_service, mock_repository, sample_user):
    sample_user.password = "hashed_secret"
    mock_repository.find_by_email.return_value = sample_user

    with pytest.raises(HTTPException) as e:
        await user_service.login_user(email="test@example.com", password="wrong")
    assert e.value.detail == "Incorrect credentials"


@pytest.mark.asyncio
async def test_update_user(user_service, mock_repository, sample_user):
    mock_repository.update.return_value = sample_user

    result = await user_service.update_user(
        user_id=sample_user.id,
        name="Updated Name"
    )

    assert isinstance(result, UserSchema)
    mock_repository.update.assert_called_once()
    args, kwargs = mock_repository.update.call_args
    assert kwargs["data"]["name"] == "Updated Name"


@pytest.mark.asyncio
async def test_update_user_password_success(user_service, mock_repository, sample_user):
    mock_repository.find_by_id.return_value = sample_user
    mock_repository.update.return_value = sample_user

    result = await user_service.update_user_password(
        user_id=sample_user.id,
        old_password="secret",
        confirm_old_password="secret",
        new_password="newsecret"
    )

    assert isinstance(result, UserSchema)
    mock_repository.update.assert_called_once()


@pytest.mark.asyncio
async def test_update_user_password_mismatch(user_service):
    with pytest.raises(HTTPException) as e:
        await user_service.update_user_password(
            user_id=uuid4(),
            old_password="secret",
            confirm_old_password="not_secret",
            new_password="newsecret"
        )
    assert e.value.detail == "Password don`t match"


@pytest.mark.asyncio
async def test_update_user_password_wrong_old(user_service, mock_repository, sample_user):
    sample_user.password = "hashed_secret"
    mock_repository.find_by_id.return_value = sample_user

    with pytest.raises(HTTPException) as e:
        await user_service.update_user_password(
            user_id=sample_user.id,
            old_password="wrong",
            confirm_old_password="wrong",
            new_password="new"
        )
    assert e.value.detail == "Password is incorrect"


@pytest.mark.asyncio
async def test_update_user_password_same_as_old(user_service, mock_repository, sample_user):
    sample_user.password = "hashed_secret"
    mock_repository.find_by_id.return_value = sample_user

    with pytest.raises(HTTPException) as e:
        await user_service.update_user_password(
            user_id=sample_user.id,
            old_password="secret",
            confirm_old_password="secret",
            new_password="secret"
        )
    assert e.value.detail == "Old password and new password are equal"
