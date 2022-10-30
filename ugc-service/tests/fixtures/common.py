import asyncio

import pytest

from src.core.config import __settings


@pytest.fixture(scope='session')
def get_server_settings_instance():
    return __settings


@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
