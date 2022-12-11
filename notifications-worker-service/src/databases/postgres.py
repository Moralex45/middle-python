from __future__ import annotations

import functools

from aiopg.connection import Connection

from src.core.settings import ServicesPostgres

auth_postgres_connection: Connection
admin_postgres_connection: Connection


@functools.lru_cache()
def get_postgres_connection(service_name: ServicesPostgres) -> Connection:
    match service_name:
        case ServicesPostgres.AUTH:
            return auth_postgres_connection
        case ServicesPostgres.ADMIN:
            return admin_postgres_connection
