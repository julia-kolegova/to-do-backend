from uuid import UUID

from sqlalchemy import select

from app.database import db
from app.repository.crud_repository import CrudRepository
from app.models.models import User


class UserRepository(CrudRepository[User, UUID]):
    async def find_by_email(self, email: str) -> User:
        stmt = select(User).where(
            User.email == email
        )

        result = await db.session.execute(stmt)
        return result.scalars().first()
