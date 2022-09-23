import pytest
import redis

from cache import RedisCacheService


@pytest.fixture()
def cache_session(settings_instance):
    redis_instance = redis.Redis(host=settings_instance.REDIS_HOST,
                                 port=settings_instance.REDIS_PORT)

    return redis_instance


@pytest.fixture()
def clean_cache(cache_session):
    keys = cache_session.keys('*')
    cache_session.delete(*keys)
