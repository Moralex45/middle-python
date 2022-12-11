from __future__ import annotations

import functools

from motor import motor_asyncio

mongodb_instance: motor_asyncio.AsyncIOMotorClient


@functools.lru_cache()
def get_mongodb_instance() -> motor_asyncio.AsyncIOMotorClient:
    return mongodb_instance
