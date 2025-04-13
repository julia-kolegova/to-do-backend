from uuid import UUID, uuid4
from typing import Optional

from pydantic import BaseModel, Field


class CreateUserSchema(BaseModel):
    name: str
    email: str
    password: str
    confirm_password: str


class UserSchema(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    email: str


class AuthUser(BaseModel):
    user: UserSchema
    access_token: str
    refresh_token: str


class UserLoginRequest(BaseModel):
    email: str
    password: str


class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None


class UserUpdatePasswordRequest(BaseModel):
    old_password: str
    confirm_old_password: str
    new_password: str
