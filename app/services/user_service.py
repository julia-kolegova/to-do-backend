from uuid import UUID
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

    async def get_user(
            self,
            user_id: UUID
    ):
        user = await self._user_crud.get_user(user_id=user_id)

        return self.__user_model_to_schema(user)

    async def login_user(self, email: str, password: str):
        user = await self._user_crud.get_user(email=email)

        hash_password = password_service.hash_password(password=password)
        if hash_password != user.password:
            raise HTTPException(status_code=400, detail="Incorrect credentials")

        return self.__user_model_to_schema(user_model=user)

    async def update_user(
            self,
            user_id: UUID,
            name: str = None,
            email: str = None
    ):
        updated_user = await self._user_crud.update_user(user_id=user_id, name=name, email=email)
        return self.__user_model_to_schema(user_model=updated_user)

    async def update_user_password(
            self,
            user_id: UUID,
            old_password: str,
            confirm_old_password: str,
            new_password: str
    ):
        print(old_password, confirm_old_password, new_password)
        if old_password != confirm_old_password:
            raise HTTPException(status_code=400, detail="Password don`t match")

        old_hash_password = password_service.hash_password(password=old_password)
        user = await self._user_crud.get_user(user_id=user_id)

        if old_hash_password != user.password:
            raise HTTPException(status_code=400, detail="Password is incorrect")

        if new_password == old_password:
            raise HTTPException(status_code=400, detail="Old password and new password are equal")

        new_hash_password = password_service.hash_password(password=new_password)

        updated_user = await self._user_crud.update_user(user_id=user_id, password=new_hash_password)
        return self.__user_model_to_schema(user_model=updated_user)
