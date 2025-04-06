from fastapi import APIRouter
from app.api.jwt import access_security, refresh_security

from app.schemas.user_schema import (
    CreateUserSchema,
    AuthUser
)

from app.services.user_service import UserService

user_service = UserService()

user_router = APIRouter(prefix='/users')
user_router.tags = ["User"]


@user_router.post('/', response_model=AuthUser)
async def create_user(new_user: CreateUserSchema):
    user = await user_service.create_user(
        name=new_user.name,
        email=new_user.email,
        password=new_user.password,
        confirm_password=new_user.confirm_password
    )

    subject = {"id": str(user.id)}
    access_token = access_security.create_access_token(subject=subject)
    refresh_token = refresh_security.create_refresh_token(subject=subject)

    auth_user = AuthUser(
        user=user,
        access_token=access_token,
        refresh_token=refresh_token
    )
    return auth_user
