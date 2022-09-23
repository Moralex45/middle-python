from http import HTTPStatus

import pytest

from src.db.services.user import UserService
from tests.functional.testdata.database_fake_data import register_users


@pytest.mark.parametrize(
    'user',
    [user for user in register_users])
def test_successful_user_registration(flask_test_client, clean_database, generate_roles_permissions, user):
    request_body = {
        'username': user['username'],
        'password': user['password']
    }
    response = flask_test_client.post('/api/v1/auth/register/', json=request_body)
    assert response.status_code == HTTPStatus.OK
    assert response.text == ''

    db_user = UserService.get_by_username(user['username'])
    assert db_user is not None
    assert db_user.username == user['username']
    assert db_user.check_password(user['password']) is True


@pytest.mark.parametrize(
    'user',
    [user for user in register_users])
def test_double_unsuccessful_user_registration(flask_test_client, clean_database, generate_roles_permissions, user):
    request_body = {
        'username': user['username'],
        'password': user['password']
    }
    response = flask_test_client.post('/api/v1/auth/register/', json=request_body)
    assert response.status_code == HTTPStatus.OK
    assert response.text == ''

    response = flask_test_client.post('/api/v1/auth/register/', json=request_body)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.text == ''
