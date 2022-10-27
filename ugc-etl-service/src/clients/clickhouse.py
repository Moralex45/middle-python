from typing import Union, Optional
from logging import Logger

from asynch import connect
from asynch.connection import Connection
from asynch.cursors import DictCursor
import backoff

from core.config import etl_logger
from models.ch_query import movie_tl_query


class ClickHouseLoader:
    def __init__(self, dsn: str, logger: Logger = etl_logger):
        self._dsn: str = dsn
        self._conn: Optional[Connection] = None
        self.logger: Logger = logger

    @backoff.on_exception(backoff.expo,
                          exception=ConnectionRefusedError,
                          logger=etl_logger,
                          max_time=10)
    async def connect(self):
        self._conn = await connect(self._dsn)
        self.logger.info('Connection to the clickhouse is established.')

    async def load_data(self, data: Union[dict, list]):
        if not data:
            pass
        if not self._conn:
            await self.connect()
        if isinstance(data, dict):
            data = [data]
        async with self._conn.cursor(cursor=DictCursor) as cursor:
            await cursor.execute(movie_tl_query, data)
            self.logger.info('Data was loaded to clickhouse')

    async def disconnect(self):
        await self._conn.close()
        self.logger.info('Connection to the clickhouse is closed.')
