from uuid import UUID

from pydantic import BaseModel


class TaskTypeResponse(BaseModel):
    id: UUID
    type_name: str
