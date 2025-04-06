from fastapi.exceptions import HTTPException

from app.models.models import User
from app.crud.user_crud import user_crud

from app.services.password_service import password_service

from app.schemas.user_schema import UserSchema


class UserService:
    def __init__(self):
        self._password_service = password_service
        self._user_crud = user_crud

    @staticmethod
    def __user_model_to_schema(user_model: User) -> UserSchema:
        return UserSchema(
            id=user_model.id,
            name=user_model.name,
            email=user_model.email
        )

    async def create_user(
            self,
            name: str,
            email: str,
            password: str,
            confirm_password: str
    ):
        if password != confirm_password:
            raise HTTPException(status_code=400, detail="Password don`t match")

        user = await self._user_crud.get_user(email=email)

        if user is not None:
            raise HTTPException(status_code=400, detail="User already exists")

        hash_password = password_service.hash_password(password=password)

        user = await self._user_crud.create_user(name=name, email=email, password=hash_password)

        return self.__user_model_to_schema(user_model=user)
