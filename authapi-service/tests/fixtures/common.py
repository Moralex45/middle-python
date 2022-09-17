import asyncio

import pytest

from tests.functional.settings import get_settings_instance


@pytest.fixture(scope='session')
async def settings_instance():
    setting_instance = get_settings_instance()
    return setting_instance
