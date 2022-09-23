from http import HTTPStatus

import pytest

from src.db.services.user import UserService
from src.db.services.auth_history import AuthHistoryService
from src import cache
from tests.functional.testdata.database_fake_data import users


@pytest.mark.parametrize(
    'user',
    [user for user in users])
def test_successful_user_login(flask_test_client,
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

    db_auth_history = AuthHistoryService.get_by_user_name(user['username'])
    assert db_auth_history is not None
    access_cookie = next(
        (cookie
         for cookie in flask_test_client.cookie_jar if cookie.name == server_settings_instance.JWT_ACCESS_COOKIE_NAME),
        None
    )
    assert access_cookie is not None
    refresh_cookie = next(
        (cookie
         for cookie in flask_test_client.cookie_jar if cookie.name == server_settings_instance.REFRESH_TOKEN_COOKIE_NAME),
        None
    )
    assert refresh_cookie is not None

    cache_service_keys = cache.cache_service.redis.keys('*')
    assert len(cache_service_keys)

    db_user = UserService.get_by_username(user['username'])
    user_refresh_token = cache_service_keys[0].decode()
    assert str(db_user.id) in user_refresh_token


@pytest.mark.parametrize(
    'user',
    [user for user in users])
def test_double_unsuccessful_user_login(flask_test_client,
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

    response = flask_test_client.post('/api/v1/auth/login/', json=request_body)

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.text == ''
