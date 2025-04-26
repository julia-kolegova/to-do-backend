from app.crud.user_crud import UserCrud
from app.crud.task_crud import TaskCrud
from app.services.password_service import PasswordService
from app.services.user_service import UserService
from app.services.task_service import TaskService


### crud ###
_user_crud = UserCrud()


def get_user_crud():
    return _user_crud


_task_crud = TaskCrud()


def get_task_crud():
    return _task_crud


### services ###
_password_service = PasswordService()


def get_password_service():
    return _password_service


_user_service = UserService(
    password_service=get_password_service(),
    user_crud=get_user_crud()
)


def get_user_service():
    return _user_service


_task_service = TaskService(
    task_crud=get_task_crud()
)


def get_task_service():
    return _task_service
