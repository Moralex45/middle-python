import typing
import uuid

import psycopg2.extras as psycopg2_extras
from aiopg.connection import Connection

import src.models.movies as movies_mdl
import src.utils.exceptions as exc


class MovieRepositoryProtocol(typing.Protocol):

    async def get_movie_by_id(self, movie_id: uuid.UUID) -> movies_mdl.Movie:
        """
        :raises NotFoundError:
        """
        ...


class MoviePostgresRepository(MovieRepositoryProtocol):

    def __init__(self,
                 connection: Connection,
                 *,
                 table_name: str):
        self._conn = connection
        self._table_name = table_name

    async def get_movie_by_id(self, movie_id: uuid.UUID) -> movies_mdl.Movie:
        query = """
            SELECT id, title FROM %s
            WHERE id = %s
        """  # noqa: Q001
        async with self._conn.cursor(cursor_factory=psycopg2_extras.DictCursor) as cur:
            await cur.execute(query, (self._table_name, movie_id))
        raw_user: dict = await cur.fetchone()
        if not raw_user:
            raise exc.NotFoundError
        return movies_mdl.Movie(**raw_user)
