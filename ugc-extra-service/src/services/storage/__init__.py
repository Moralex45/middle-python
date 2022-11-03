import functools

from motor import motor_asyncio

mongodb_instance: motor_asyncio.AsyncIOMotorClient | None = None


@functools.lru_cache()
def get_kafka() -> motor_asyncio.AsyncIOMotorClient | None:
    return mongodb_instance
