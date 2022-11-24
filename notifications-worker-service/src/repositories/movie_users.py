import typing
import uuid

from asynch.connection import Connection
from asynch.cursors import DictCursor


class MovieUsersRepositoryProtocol(typing.Protocol):

    def get_movie_viewers(self, movie_id: uuid.UUID) -> typing.AsyncIterator[list[uuid.UUID] | None]:
        ...


class MovieUserClickhouseRepository(MovieUsersRepositoryProtocol):

    def __init__(self,
                 connection: Connection,
                 *,
                 db_table: str,
                 batch_size: int = 10_000) -> None:
        self._conn = connection
        self._db_table = db_table
        self._batch_size = batch_size

    async def get_movie_viewers(self, movie_id: uuid.UUID) -> typing.AsyncIterator[list[uuid.UUID] | None]:
        async with self._conn.cursor(cursor=DictCursor) as cursor:
            query = """
                SELECT user_id FROM %(db_table)s
                WHERE movie_id == %(movie_id)s
            """  # noqa: Q001
            await cursor.execute(query, {'movie_id': movie_id, 'db_table': self._db_table})
            while users_id := await cursor.fetchmany(self._batch_size):
                yield list(users_id.values())
            yield None
