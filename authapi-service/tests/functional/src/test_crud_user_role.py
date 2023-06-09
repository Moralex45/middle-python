import uuid

import pytest

from tests.functional.testdata.database_fake_data import roles, users_roles, users
from http import HTTPStatus


@pytest.mark.parametrize(
    'user_role',
    [user_role for user_role in users_roles])
def test_scrap_existing_user_role(super_user_authenticated_flask_test_client,
                                  clean_database,
                                  generate_users_roles,
                                  user_role):
    response = super_user_authenticated_flask_test_client.get(f'/api/v1/crud/user_role/{user_role["id"]}')
    assert response.status_code == HTTPStatus.OK
    assert response.is_json
    assert response.json == user_role


def test_scrap_non_existing_user_role(super_user_authenticated_flask_test_client,
                                      clean_database,
                                      generate_users_roles):
    response = super_user_authenticated_flask_test_client.get(f'/api/v1/crud/user_role/{uuid.uuid4()}')
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response.text == ''


@pytest.mark.parametrize(
    'user',
    [user for user in users])
def test_scrap_existing_user_role_filtered_by_user_id(super_user_authenticated_flask_test_client,
                                                      clean_database,
                                                      generate_users_roles,
                                                      user):
    response = super_user_authenticated_flask_test_client.get(f'/api/v1/crud/user_role/?user_id={user["id"]}')
    assert response.status_code == HTTPStatus.OK
    assert response.is_json
    assert response.json == list(filter(lambda o: o['user_id'] == user['id'], users_roles))


def test_scrap_non_existing_user_role_filtered_by_role_id(super_user_authenticated_flask_test_client,
                                                          clean_database,
                                                          generate_users_roles):
    response = super_user_authenticated_flask_test_client.get(f'/api/v1/crud/user_role/?user_id={uuid.uuid4()}')
    assert response.status_code == HTTPStatus.OK
    assert response.is_json
    assert response.json == []


def test_scrap_user_role_filtered_by_inappropriate_role_id_format(super_user_authenticated_flask_test_client,
                                                                  clean_database,
                                                                  generate_users_roles,
                                                                  server_settings_instance):
    response = super_user_authenticated_flask_test_client.get(
        f'/api/v1/crud/user_role/?user_id={str(uuid.uuid4())[-1:]}'
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.text == ''


@pytest.mark.parametrize(
    'user_role',
    [user_role for user_role in users_roles])
def test_create_user_role(super_user_authenticated_flask_test_client,
                          clean_database,
                          generate_roles_permissions,
                          generate_users,
                          user_role):
    request_body = {
        'user_id': user_role['user_id'],
        'role_id': user_role['role_id']
    }
    response = super_user_authenticated_flask_test_client.post('/api/v1/crud/user_role/', json=request_body)
    assert response.status_code == HTTPStatus.OK
    assert response.is_json

    created_user_role_id = response.json['id']
    response = super_user_authenticated_flask_test_client.get(f'/api/v1/crud/user_role/{created_user_role_id}')
    assert response.status_code == HTTPStatus.OK
    assert response.is_json
    request_body |= {
        'id': created_user_role_id
    }
    assert response.json == request_body


def test_double_create_user_role(super_user_authenticated_flask_test_client,
                                 clean_database,
                                 generate_roles_permissions,
                                 generate_users):
    user_role = users_roles[0]
    request_body = {
        'user_id': user_role['user_id'],
        'role_id': user_role['role_id']
    }
    response = super_user_authenticated_flask_test_client.post('/api/v1/crud/user_role/', json=request_body)
    assert response.status_code == HTTPStatus.OK
    assert response.is_json

    response = super_user_authenticated_flask_test_client.post('/api/v1/crud/user_role/', json=request_body)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.text == ''


@pytest.mark.parametrize(
    'user_id, role_id',
    [(users[0]['id'], uuid.uuid4()),
     (uuid.uuid4(), roles[0]['id']),
     (uuid.uuid4(), uuid.uuid4())])
def test_create_user_role_with_non_existent_parameters(super_user_authenticated_flask_test_client,
                                                       clean_database,
                                                       generate_roles_permissions,
                                                       generate_users,
                                                       user_id, role_id):
    request_body = {
        'user_id': user_id,
        'role_id': role_id,
    }
    response = super_user_authenticated_flask_test_client.post('/api/v1/crud/user_role/', json=request_body)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.text == ''


@pytest.mark.parametrize(
    'user_role',
    [user_role for user_role in users_roles])
def test_delete_existing_user_role(super_user_authenticated_flask_test_client,
                                   clean_database,
                                   generate_users_roles,
                                   user_role):
    response = super_user_authenticated_flask_test_client.delete(f'/api/v1/crud/user_role/{user_role["id"]}')
    assert response.status_code == HTTPStatus.OK
    assert response.text == ''

    response = super_user_authenticated_flask_test_client.get(f'/api/v1/crud/user_role/{user_role["id"]}')
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response.text == ''


def test_delete_non_existing_user_role(super_user_authenticated_flask_test_client,
                                       clean_database,
                                       generate_users_roles):
    response = super_user_authenticated_flask_test_client.delete(f'/api/v1/crud/user_role/{uuid.uuid4()}')
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.text == ''
