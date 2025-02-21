from typing import Protocol, Annotated

from fastapi import Depends

from sqlalchemy import insert, select


from src.auth.models import User
from src.auth.schemas import UserSchema
from src.database import connection


class UserRepositoryProtocol(Protocol):

    async def add_user(self, session, data: dict) -> UserSchema:
        ...

    async def get_user_by_email(self, session, email: str) -> UserSchema:
        ...

    async def get_all_users(self, session):
        ...

    async def get_id_by_email(self, email):
        ...

    async def get_user_status_by_id(self, user_id):
        ...


class UserRepositoryImp:

    @connection
    async def get_user_status_by_id(self, user_id: int, session):

        stmt = select(User).where(User.id == int(user_id))

        result = await session.execute(stmt)
        result = [row[0].to_read_model() for row in result.all()]

        if result:
            return result[0].status


    @connection
    async def add_user(self, data: dict, session) -> list:

        stmt = insert(User).values(**data).returning(User)
        result = await session.execute(stmt)
        new_user = [row[0].to_read_model() for row in result.all()]
        await session.commit()

        return new_user

    @connection
    async def get_user_by_email(self, email: str, session):

        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        result = [row[0] for row in result.all()]
        return result

    @connection
    async def get_all_users(self, session):
        stmt = select(User)
        result = await session.execute(stmt)
        result = [row[0].to_read_model() for row in result.all()]

        return result

    @connection
    async def get_id_by_email(self, email: str, session) -> int:
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        result = [row[0].to_read_model() for row in result.all()]

        if result:
            return result[0].id

async def get_user_repository() -> UserRepositoryProtocol:
    return UserRepositoryImp()


UserRepository = Annotated[UserRepositoryProtocol, Depends(get_user_repository)]