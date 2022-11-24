import typing
import uuid

import psycopg2.extras as psycopg2_extras
from aiopg.connection import Connection

import src.models.users as users_mdl
import src.utils.exceptions as exc


class UsersRepositoryProtocol(typing.Protocol):

    async def get_user_by_id(self, user_id: uuid.UUID) -> users_mdl.User:
        """
        :raises NotFoundError:
        """
        ...

    def get_all_users(self) -> typing.AsyncIterator[list[users_mdl.User] | None]:
        ...

    async def get_specified_users(self, users_id: list[uuid.UUID]) -> list[users_mdl.User]:
        """
        :raises NotFoundError:
        """
        ...


class UsersPostgresRepository(UsersRepositoryProtocol):

    def __init__(self,
                 connection: Connection,
                 *,
                 table_name: str,
                 batch_size: int = 10_000):
        self._conn = connection
        self._table_name = table_name
        self._batch_size = batch_size

    async def get_user_by_id(self, user_id: uuid.UUID) -> users_mdl.User:
        query = """
            SELECT * FROM %s
            WHERE user_id = %s
        """  # noqa: Q001
        async with self._conn.cursor(cursor_factory=psycopg2_extras.DictCursor) as cur:
            await cur.execute(query, (self._table_name, user_id))
            raw_user: dict = await cur.fetchone()
        if not raw_user:
            raise exc.NotFoundError
        return users_mdl.User(**raw_user)

    async def get_all_users(self) -> typing.AsyncIterator[list[users_mdl.User] | None]:
        query = """
            SELECT * FROM %s
        """  # noqa: Q001
        async with self._conn.cursor(cursor_factory=psycopg2_extras.DictCursor) as cur:
            await cur.execute(query, (self._table_name,))
            while users := await cur.fetchmany(self._batch_size):
                yield [users_mdl.User(**user) for user in users]
        yield None

    async def get_specified_users(self, users_id: list[uuid.UUID]) -> list[users_mdl.User]:
        query = """
            SELECT * FROM %s
            WHERE user_id IN %s
        """  # noqa: Q001
        async with self._conn.cursor(cursor_factory=psycopg2_extras.DictCursor) as cur:
            await cur.execute(query, (self._table_name, tuple(users_id)))
            raw_users: list[dict] = await cur.fetchall()
        if not raw_users:
            raise exc.NotFoundError
        return [users_mdl.User(**user) for user in raw_users]
