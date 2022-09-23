
import pytest
from src.app_utils import create_raw_app


@pytest.fixture()
def flask_app():
    return create_raw_app()


@pytest.fixture()
def flask_test_client(flask_app, server_settings_instance):
    client = flask_app.test_client()

    return client
