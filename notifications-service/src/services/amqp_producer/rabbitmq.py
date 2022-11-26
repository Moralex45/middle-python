from __future__ import annotations

import functools

import aio_pika

rabbitmq_connection: aio_pika.RobustConnection | None = None


@functools.lru_cache()
def get_rabbitmq_connection_instance() -> aio_pika.RobustConnection | None:
    return rabbitmq_connection
