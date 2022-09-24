from http import HTTPStatus

import pytest

from src import cache
from tests.functional.testdata.database_fake_data import users, user_agents


@pytest.mark.parametrize(
    'user',
    [user for user in users])
def test_successful_user_logout_base(flask_test_client,
                                     clean_database,
                                     clean_cache,
                                     generate_users,
                                     server_settings_instance,
                                     user):
    request_body = {
        'username': user['username'],
        'password': user['password'],
        'remember': True
    }
    response = flask_test_client.post('/api/v1/auth/login/', json=request_body)

    assert response.status_code == HTTPStatus.OK
    assert response.text == ''

    request_body = {}
    response = flask_test_client.post('/api/v1/auth/logout/', json=request_body)

    assert response.status_code == HTTPStatus.OK
    assert response.text == ''

    cache_service_keys = cache.cache_service.redis.keys('*')
    assert len(cache_service_keys) == 0

    response = flask_test_client.post('/api/v1/auth/logout/', json=request_body)

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.parametrize(
    'user',
    [user for user in users])
def test_successful_user_logout_multiply_devices(flask_test_client,
                                                 clean_database,
                                                 clean_cache,
                                                 generate_users,
                                                 server_settings_instance,
                                                 user):
    for user_agent in user_agents:
        request_body = {
            'username': user['username'],
            'password': user['password'],
            'remember': True
        }
        response = flask_test_client.post('/api/v1/auth/login/',
                                          json=request_body,
                                          environ_base={'HTTP_USER_AGENT': user_agent})

        assert response.status_code == HTTPStatus.OK
        assert response.text == ''

    request_body = {
        'all_devices': True
    }
    response = flask_test_client.post('/api/v1/auth/logout/', json=request_body)

    assert response.status_code == HTTPStatus.OK
    assert response.text == ''

    cache_service_keys = cache.cache_service.redis.keys('*')
    assert len(cache_service_keys) == 0

    response = flask_test_client.post('/api/v1/auth/logout/', json=request_body)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
