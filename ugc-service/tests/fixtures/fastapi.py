import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture(scope='session')
def get_web_test_client() -> TestClient:
    with TestClient(app) as client:
        yield client
