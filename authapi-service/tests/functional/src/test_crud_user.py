import pytest

from db.services.permissions import PermissionService
from src.db.services.user import UserService
from src.db.services.userdata import UserDataService
from tests.functional.testdata.database_fake_data import users, permissions
from http import HTTPStatus


@pytest.mark.parametrize(
    'user',
    [user for user in users])
def test_successful_user_update_data(flask_test_client, clean_database, generate_roles_permissions, user):
    request_body = {
        'username': user['username'],
        'password': user['password']
    }
    response = flask_test_client.post('/api/v1/auth/register/', json=request_body)
    assert response.status_code == HTTPStatus.OK
    assert response.text == ''

    request_body = {
        'username': user['username'],
        'password': user['password'],
        'remember': True
    }
    response = flask_test_client.post('/api/v1/auth/login/', json=request_body)

    assert response.status_code == HTTPStatus.OK
    assert response.text == ''

    request_body = {
        'password': user['password']
    }

    update_fields = {
        'first_name': 'sample2',
        'last_name': 'sample3',
        'email': 'sample@sample.com',
        'birth_date': 1516239022
    }

    for update_field_key, update_field_item in update_fields.items():
        update_field_request_body = request_body | {update_field_key: update_field_item}

        db_user = UserService.get_by_username(user['username'])
        db_userdata = UserDataService.get_by_user_id(db_user.id)
        userdata_field_before_update = db_userdata.__dict__[update_field_key]

        response = flask_test_client.post('/api/v1/crud/user/', json=update_field_request_body)

        assert response.status_code == HTTPStatus.OK
        assert response.text == ''

        db_userdata = UserDataService.get_by_user_id(db_user.id)
        userdata_field_after_update = db_userdata.__dict__[update_field_key]

        assert userdata_field_before_update != userdata_field_after_update

    update_field = {
        'user_name': 'sample2'
    }

    update_field_request_body = request_body | update_field

    username_before_update = UserService.get_by_username(user['username']).username
    response = flask_test_client.post('/api/v1/crud/user/', json=update_field_request_body)

    assert response.status_code == HTTPStatus.OK
    assert response.text == ''

    db_user = UserService.get_by_username(update_field['user_name'])

    assert db_user is not None
    assert username_before_update != db_user.username

    new_user_user_name = update_field['user_name']

    update_field = {
        'new_password': 'sample1'
    }

    update_field_request_body = request_body | update_field

    db_user = UserService.get_by_username(new_user_user_name)

    assert db_user.check_password(user['password']) is True

    response = flask_test_client.post('/api/v1/crud/user/', json=update_field_request_body)

    assert response.status_code == HTTPStatus.OK
    assert response.text == ''

    db_user = UserService.get_by_username(new_user_user_name)

    assert db_user.check_password(user['password']) is False
    assert db_user.check_password(update_field['new_password']) is True


@pytest.mark.parametrize(
    'user',
    [user for user in users])
def test_get_user_permissions_correct_users(flask_test_client,
                                            clean_database,
                                            clean_cache,
                                            generate_roles_permissions,
                                            server_settings_instance,
                                            user):
    request_body = {
        'username': user['username'],
        'password': user['password']
    }
    response = flask_test_client.post('/api/v1/auth/register/', json=request_body)
    assert response.status_code == HTTPStatus.OK
    assert response.text == ''

    db_user = UserService.get_by_username(user['username'])

    user_permissions = PermissionService.get_filtered_by_user_id(db_user.id)
    query = ''
    for user_permission in user_permissions:
        query += f'permission={user_permission.code}&'

    response = flask_test_client.post(f'/api/v1/crud/user/{db_user.id}/check_permissions?{query[:-1]}')

    assert response.status_code == HTTPStatus.OK
    assert response.is_json
    assert response.json == {'result': True}


@pytest.mark.parametrize(
    'user',
    [user for user in users])
@pytest.mark.parametrize(
    'permission',
    [permission for permission in permissions])
def test_get_user_permissions_incorrect_permissions(flask_test_client,
                                                    clean_database,
                                                    clean_cache,
                                                    generate_roles_permissions,
                                                    server_settings_instance,
                                                    user, permission):
    request_body = {
        'username': user['username'],
        'password': user['password']
    }
    response = flask_test_client.post('/api/v1/auth/register/', json=request_body)
    assert response.status_code == HTTPStatus.OK
    assert response.text == ''

    db_user = UserService.get_by_username(user['username'])
    expected_status_code = HTTPStatus.OK

    user_permissions = PermissionService.get_filtered_by_user_id(db_user.id)
    query = f'permission={permission["code"]}&'
    for user_permission in user_permissions:
        if user_permission.code == permission['code']:
            query = ''
            expected_status_code = HTTPStatus.BAD_REQUEST

    response = flask_test_client.post(f'/api/v1/crud/user/{db_user.id}/check_permissions?{query[:-1]}')

    assert response.status_code == expected_status_code
    if expected_status_code == HTTPStatus.OK:
        assert response.is_json
        assert response.json == {'result': False}
    else:
        assert response.text == ''
