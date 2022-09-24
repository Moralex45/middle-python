from http import HTTPStatus

import pytest

from src.db.services.user import UserService
from src.db.services.auth_history import AuthHistoryService
from src import cache
from tests.functional.testdata.database_fake_data import users, roles


@pytest.mark.parametrize(
    'user',
    [user for user in users])
def test_successful_refresh(flask_test_client,
                            clean_database,
                            generate_roles_permissions,
                            generate_users,
                            user):
    request_body = {
        'username': user['username'],
        'password': user['password'],
        'remember': True
    }
    response = flask_test_client.post('/api/v1/auth/login/', json=request_body)

    assert response.status_code == HTTPStatus.OK
    assert response.text == ''

    db_user = UserService.get_by_username(user['username'])
    db_auth_history = AuthHistoryService.get_by_user_name(user['username'])[0]
    session = cache.cache_service.get_user_sessions_by_user_id(db_user.id)[0]

    response = flask_test_client.post('/api/v1/auth/refresh/')

    assert response.status_code == HTTPStatus.OK
    assert response.text == ''

    refreshed_db_auth_history = AuthHistoryService.get_by_user_name(user['username'])[0]
    refreshed_session = cache.cache_service.get_user_sessions_by_user_id(db_user.id)[0]

    assert session != refreshed_session
    assert db_auth_history.date_start != refreshed_db_auth_history.date_start
