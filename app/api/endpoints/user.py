from fastapi import APIRouter, Depends
from app.api.jwt import access_security, refresh_security, get_jwt_token, refresh_jwt_token

from app.schemas.user_schema import (
    CreateUserSchema,
    AuthUser,
    UserSchema,
    UserLoginRequest,
    UserUpdateRequest,
    UserUpdatePasswordRequest
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


@user_router.get('/', response_model=UserSchema)
async def get_user(credentials: dict = Depends(get_jwt_token)):
    user_id = credentials["id"]
    user = await user_service.get_user(user_id=user_id)
    return user


@user_router.post('/login', response_model=AuthUser)
async def login_user(user: UserLoginRequest):
    user = await user_service.login_user(email=user.email, password=user.password)

    subject = {"id": str(user.id)}
    access_token = access_security.create_access_token(subject=subject)
    refresh_token = refresh_security.create_refresh_token(subject=subject)

    auth_user = AuthUser(
        user=user,
        access_token=access_token,
        refresh_token=refresh_token
    )
    return auth_user


@user_router.patch('/', response_model=UserSchema)
async def update_user(new_user_data: UserUpdateRequest, credentials: dict = Depends(get_jwt_token)):
    user_id = credentials["id"]
    user = await user_service.update_user(user_id=user_id, email=new_user_data.email, name=new_user_data.name)
    return user


@user_router.patch('/password', response_model=UserSchema)
async def update_user_password(new_password: UserUpdatePasswordRequest, credentials: dict = Depends(get_jwt_token)):
    user_id = credentials["id"]

    updated_user = await user_service.update_user_password(
        user_id=user_id,
        old_password=new_password.old_password,
        confirm_old_password=new_password.confirm_old_password,
        new_password=new_password.new_password
    )
    return updated_user


@user_router.get('/token/refresh')
async def refresh_token(credentials: dict = Depends(refresh_jwt_token)):
    access_token = access_security.create_access_token(subject=credentials)
    return {"access_token": access_token}
