import typing
import uuid

import asyncpg

import src.models.users as users_mdl
import src.utils.exceptions as exc


class UsersRepositoryProtocol(typing.Protocol):

    async def get_user_by_id(self, user_id: uuid.UUID) -> users_mdl.User:
        ...

    async def get_all_users(self) -> list[users_mdl.User]:
        ...


class UsersPostgresRepository(UsersRepositoryProtocol):

    def __init__(self,
                 connection: asyncpg.Connection,
                 table_name: str):
        self.__conn = connection
        self.__table_name = table_name

    async def get_user_by_id(self, user_id: uuid.UUID) -> users_mdl.User:
        query = """
            SELECT * FROM $1
            WHERE user_id = $2
        """  # noqa: Q001
        raw_user: asyncpg.Record = await self.__conn.fetchrow(query, self.__table_name, user_id)
        if raw_user is None:
            raise exc.NotFoundError
        return users_mdl.User(**raw_user)

    async def get_all_users(self) -> list[users_mdl.User]:
        query = """
            SELECT * FROM $1
        """  # noqa: Q001
        return [users_mdl.User(**user) for user in await self.__conn.fetch(query, self.__table_name)]
