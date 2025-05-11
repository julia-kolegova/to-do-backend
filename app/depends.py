from app.repository.task_type_repository import TaskTypeRepository
from app.repository.user_repository import UserRepository
from app.repository.task_repository import TaskRepository
from app.services.password_service import PasswordService
from app.services.user_service import UserService
from app.services.task_service import TaskService
from app.services.task_type_service import TaskTypeService


### repository ###
_task_type_repository = TaskTypeRepository()


def get_task_type_repository() -> TaskTypeRepository:
    return _task_type_repository


_task_repository = TaskRepository()


def get_task_repository() -> TaskRepository:
    return _task_repository


_user_repository = UserRepository()


def get_user_repository() -> UserRepository:
    return _user_repository


### services ###
_password_service = PasswordService()


def get_password_service() -> PasswordService:
    return _password_service


_user_service = UserService(
    password_service=get_password_service(),
    user_repository=get_user_repository()
)


def get_user_service() -> UserService:
    return _user_service


_task_service = TaskService(
    task_repository=get_task_repository()
)


def get_task_service() -> TaskService:
    return _task_service


_task_type_service = TaskTypeService(
    task_type_repository=get_task_type_repository()
)


def get_task_type_service() -> TaskTypeService:
    return _task_type_service

