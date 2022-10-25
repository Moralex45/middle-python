import asyncio

import aiohttp
import pytest

from tests.functional.settings import get_settings_instance


@pytest.fixture(scope='session')
async def settings_instance():
    setting_instance = get_settings_instance()
    return setting_instance


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()
