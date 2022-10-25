import pytest
import redis


@pytest.fixture()
def cache_session(server_settings_instance):
    redis_instance = redis.Redis(host=server_settings_instance.REDIS_HOST,
                                 port=server_settings_instance.REDIS_PORT)

    return redis_instance


@pytest.fixture()
def clean_cache(cache_session):
    keys = cache_session.keys('*')
    if len(keys):
        cache_session.delete(*keys)
