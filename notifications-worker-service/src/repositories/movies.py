import typing
import uuid

import asyncpg

import src.models.movies as movies_mdl
import src.utils.exceptions as exc


class MovieRepositoryProtocol(typing.Protocol):

    async def get_movie_by_id(self, movie_id: uuid.UUID) -> movies_mdl.Movie:
        ...


class MoviePostgresRepository(MovieRepositoryProtocol):

    def __init__(self,
                 connection: asyncpg.Connection,
                 table_name: str):
        self.__conn = connection
        self.__table_name = table_name

    async def get_movie_by_id(self, movie_id: uuid.UUID) -> movies_mdl.Movie:
        query = """
            SELECT id, title FROM $1
            WHERE id = $2
        """  # noqa: Q001
        raw_user: asyncpg.Record = await self.__conn.fetchrow(query, self.__table_name, movie_id)
        if raw_user is None:
            raise exc.NotFoundError
        return movies_mdl.Movie(**raw_user)
