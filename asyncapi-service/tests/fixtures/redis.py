import aioredis
import pytest
from aioredis import Redis

from tests.functional.settings import TestSettings


@pytest.fixture(scope='session')
async def redis_client(settings_instance: TestSettings):
    redis_pool = await aioredis.create_redis(
        (settings_instance.REDIS_HOST, settings_instance.REDIS_PORT))
    yield redis_pool
    redis_pool.close()
    await redis_pool.wait_closed()


@pytest.fixture(scope='session')
async def flush_db(redis_client: Redis):
    await redis_client.flushall()
