import pytest

from src.core.config import get_settings_instance as server_setting_instance


@pytest.fixture()
def server_settings_instance():
    setting_instance = server_setting_instance()
    return setting_instance
