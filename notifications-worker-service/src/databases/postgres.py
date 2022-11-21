from __future__ import annotations

import functools

import asyncpg

from src.core.settings import ServicesPostgres

auth_postgres_connection: asyncpg.Connection | None = None
admin_postgres_connection: asyncpg.Connection | None = None


@functools.lru_cache()
def get_postgres_connection(service_name: ServicesPostgres) -> asyncpg.Connection | None:
    match service_name:
        case ServicesPostgres.AUTH:
            return auth_postgres_connection
        case ServicesPostgres.ADMIN:
            return admin_postgres_connection
