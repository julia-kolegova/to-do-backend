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

    async def update_user(self):
        pass


user_crud = UserCrud()
