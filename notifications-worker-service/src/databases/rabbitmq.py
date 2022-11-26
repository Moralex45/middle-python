from __future__ import annotations

import functools

from aio_pika.abc import AbstractConnection

rabbitmq_instance: AbstractConnection


@functools.lru_cache()
def get_rabbitmq_instance() -> AbstractConnection:
    return rabbitmq_instance
