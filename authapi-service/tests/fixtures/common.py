import pytest

from tests.functional.settings import get_settings_instance as test_setting_instance
from src.core.config import get_settings_instance as server_setting_instance


@pytest.fixture()
def settings_instance():
    setting_instance = test_setting_instance()
    return setting_instance


@pytest.fixture()
def server_settings_instance():
    setting_instance = server_setting_instance()
    return setting_instance
