
import pytest
from src.app_utils import create_raw_app


@pytest.fixture(scope='session')
def flask_app():
    return create_raw_app()


@pytest.fixture(scope='session')
def flask_test_client(flask_app):
    return flask_app.test_client()
