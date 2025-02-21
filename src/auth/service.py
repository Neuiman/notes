from typing import Protocol, Annotated

from fastapi.params import Depends

from src.auth.crypto_heandlers import check_user, create_user_register_hash_schema
from src.auth.schemas import UserRegisterSchema
from src.auth.repository import UserRepositoryProtocol, get_user_repository, UserRepository
from src.auth.schemas import UserLoginSchema


class UserServiceProtocol(Protocol):

    async def add_new_user(self, user: UserRegisterSchema):
        ...

    async def verify_user(self, user: UserLoginSchema):
        ...

    async def get_all_users(self):
        ...

    async def get_id(self, email: str):
        ...

    async def get_user_status_by_id(self, user_id: int):
        ...


class UserServiceImp:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_user_status_by_id(self, user_id: int):

        return await self.user_repository.get_user_status_by_id(user_id)

    async def add_new_user(self, user: UserRegisterSchema):
        user = await create_user_register_hash_schema(user)
        user_dict = user.model_dump()
        new_user = await self.user_repository.add_user(user_dict)

        return new_user

    async def verify_user(self, user: UserLoginSchema) -> bool | dict:
        try:
            user_from_db = await self.user_repository.get_user_by_email(user.email)
            is_user_verified = await check_user(user, user_from_db[0])

            return is_user_verified
        except:
            return False

    async def get_id(self, email: str) -> dict:

        return await self.user_repository.get_id_by_email(email)

    async def all_users(self):

        return await self.user_repository.get_all_users()

async def get_user_service(user_repository: UserRepository) -> UserServiceProtocol:
    return UserServiceImp(user_repository)


UserService = Annotated[UserServiceProtocol, Depends(get_user_service)]

