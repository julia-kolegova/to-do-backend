from app.repository.task_type_repository import TaskTypeRepository


class TaskTypeService:
    def __init__(
            self,
            task_type_repository: TaskTypeRepository
    ):
        self._task_type_repository = task_type_repository
