from __future__ import annotations

import functools

from asynch.connection import Connection  # type: ignore

clickhouse_connection: Connection


@functools.lru_cache()
def get_clickhouse_connection() -> Connection:
    return clickhouse_connection
