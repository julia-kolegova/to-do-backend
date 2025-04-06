from fastapi_sqlalchemy import db


class DBOperations:
    @staticmethod
    async def db_write(entity):
        db.session.add(entity)
        db.session.commit()

    @staticmethod
    async def db_update():
        db.session.commit()

    @staticmethod
    async def db_delete(entity):
        db.session.delete(entity)
        db.session.commit()

    @staticmethod
    async def refresh(entity):
        db.session.refresh(entity)
