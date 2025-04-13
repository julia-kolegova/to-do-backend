from datetime import datetime
from uuid import UUID, uuid4

from fastapi_sqlalchemy import db

from app.crud.db_operations import DBOperations

from app.models.models import User


class UserCrud(DBOperations):
    @staticmethod
    async def get_user(user_id: UUID = None, email: str = None) -> User | None:
        user = None

        if email is not None:
            user = db.session.query(User).filter(User.email == email).first()
        elif user_id is not None:
            user = db.session.query(User).filter(User.id == user_id).first()

        return user

    async def create_user(self, name: str, email: str, password: str) -> User:
        user = User(
            id=uuid4(),
            name=name,
            email=email,
            password=password,
            created_at=datetime.now()
        )

        await self.db_write(user)
        await self.refresh(user)

        return user

    async def update_user(
            self,
            user_id: UUID,
            name: str = None,
            email: str = None,
            password: str = None
    ):
        user = await self.get_user(user_id=user_id)

        if name is not None:
            user.name = name
        if email is not None:
            user.email = email
        if password is not None:
            user.password = password

        await self.db_update()
        await self.refresh(user)

        return user


user_crud = UserCrud()
