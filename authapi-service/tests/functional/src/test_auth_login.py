from http import HTTPStatus

import pytest

from functional.testdata.database_fake_data import register_users


@pytest.mark.parametrize(
    'user',
    [user for user in register_users])
def test_successful_user_registration(flask_test_client, clean_database, clean_cache, user):
    request_body = {
        'username': user['username'],
        'password': user['password'],
        'remember': True
    }
    response = flask_test_client.post('/api/v1/auth/login/', json=request_body)

    assert response.status_code == HTTPStatus.OK
    assert response.text == ''

    db_user = UserService.get_by_username(user['username'])
    assert db_user is not None
    assert db_user.username == user['username']
    assert db_user.check_password(user['password']) is True