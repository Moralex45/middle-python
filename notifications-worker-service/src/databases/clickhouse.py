from __future__ import annotations

import functools

from asynch.connection import Connection

clickhouse_connection: Connection | None = None


@functools.lru_cache()
def get_clickhouse_connection() -> Connection | None:
    return clickhouse_connection
