import typing
import uuid

from asynch.connection import Connection
from asynch.cursors import DictCursor


class MovieUsersRepositoryProtocol(typing.Protocol):

    async def get_movie_viewers(self, movie_id: uuid.UUID) -> list[uuid.UUID]:
        ...


class ClickhouseMovieUserRepository(MovieUsersRepositoryProtocol):

    def __init__(self,
                 connection: Connection,
                 db_table: str):
        self.__conn = connection
        self.__db_table = db_table

    async def get_movie_viewers(self, movie_id: uuid.UUID) -> list[uuid.UUID]:
        async with self.__conn.cursor(cursor=DictCursor) as cursor:
            query = """
                SELECT user_id FROM %(db_table)s
                WHERE movie_id == %(movie_id)s
            """  # noqa: Q001
            await cursor.execute(query, {'movie_id': movie_id, 'db_table': self.__db_table})
            users_id = await cursor.fetchall()
            return list(users_id.values())
