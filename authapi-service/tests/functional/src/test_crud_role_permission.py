import uuid

import pytest

from tests.functional.testdata.database_fake_data import roles_permissions, roles, permissions
from http import HTTPStatus


@pytest.mark.parametrize(
    'role_permission',
    [role_permission for role_permission in roles_permissions])
def test_scrap_existing_roles_permissions(super_user_authenticated_flask_test_client,
                                          clean_database,
                                          generate_roles_permissions,
                                          role_permission):
    response = super_user_authenticated_flask_test_client.get(f'/api/v1/crud/role_permission/{role_permission["id"]}')
    assert response.status_code == HTTPStatus.OK
    assert response.is_json
    assert response.json == role_permission


def test_scrap_non_existing_roles_permissions(super_user_authenticated_flask_test_client,
                                              clean_database,
                                              generate_roles_permissions):
    response = super_user_authenticated_flask_test_client.get(f'/api/v1/crud/role_permission/{uuid.uuid4()}')
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response.text == ''


def test_scrap_existing_roles_permissions_filtered_by_role_id(super_user_authenticated_flask_test_client,
                                                              clean_database,
                                                              generate_roles_permissions):
    role = roles[0]
    response = super_user_authenticated_flask_test_client.get(f'/api/v1/crud/role_permission/?role_id={role["id"]}')
    assert response.status_code == HTTPStatus.OK
    assert response.is_json
    assert response.json == list(filter(lambda o: o['role_id'] == role['id'], roles_permissions))


def test_scrap_non_existing_roles_permissions_filtered_by_role_id(super_user_authenticated_flask_test_client,
                                                                  clean_database,
                                                                  generate_roles_permissions):
    response = super_user_authenticated_flask_test_client.get(f'/api/v1/crud/role_permission/?role_id={uuid.uuid4()}')
    assert response.status_code == HTTPStatus.OK
    assert response.is_json
    assert response.json == []


def test_scrap_roles_permissions_filtered_by_inappropriate_role_id_format(super_user_authenticated_flask_test_client,
                                                                          clean_database,
                                                                          generate_roles_permissions):
    response = super_user_authenticated_flask_test_client.get(
        f'/api/v1/crud/role_permission/?role_id={str(uuid.uuid4())[-1:]}'
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.text == ''


def test_delete_existing_roles_permissions(super_user_authenticated_flask_test_client,
                                           clean_database,
                                           generate_roles_permissions):
    role_permission = roles_permissions[0]
    response = super_user_authenticated_flask_test_client.delete(
        f'/api/v1/crud/role_permission/{role_permission["id"]}'
    )
    assert response.status_code == HTTPStatus.OK
    assert response.text == ''

    response = super_user_authenticated_flask_test_client.get(f'/api/v1/crud/role_permission/{role_permission["id"]}')
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response.text == ''


def test_delete_non_existing_roles_permissions(super_user_authenticated_flask_test_client,
                                               clean_database,
                                               generate_roles_permissions):
    response = super_user_authenticated_flask_test_client.delete(f'/api/v1/crud/role_permission/{uuid.uuid4()}')
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.text == ''


def test_create_role_permission(super_user_authenticated_flask_test_client,
                                clean_database,
                                generate_roles,
                                generate_permissions):
    role = roles[0]
    permission = permissions[0]
    request_body = {
        'role_id': role['id'],
        'permission_id': permission['id']
    }
    response = super_user_authenticated_flask_test_client.post('/api/v1/crud/role_permission/', json=request_body)
    assert response.status_code == HTTPStatus.OK
    assert response.is_json

    created_role_permission_id = response.json['id']
    response = super_user_authenticated_flask_test_client.get(
        f'/api/v1/crud/role_permission/{created_role_permission_id}'
    )
    assert response.status_code == HTTPStatus.OK
    assert response.is_json

    request_body |= {'id': created_role_permission_id}
    assert response.json == request_body


def test_double_create_role_permission(super_user_authenticated_flask_test_client,
                                       clean_database,
                                       generate_roles,
                                       generate_permissions):
    role = roles[0]
    permission = permissions[0]
    request_body = {
        'role_id': role['id'],
        'permission_id': permission['id']
    }
    response = super_user_authenticated_flask_test_client.post('/api/v1/crud/role_permission/', json=request_body)
    assert response.status_code == HTTPStatus.OK
    assert response.is_json

    response = super_user_authenticated_flask_test_client.post('/api/v1/crud/role_permission/', json=request_body)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.text == ''


@pytest.mark.parametrize(
    'role_id, permission_id',
    [(roles[0]['id'], uuid.uuid4()),
     (uuid.uuid4(), permissions[0]['id']),
     (uuid.uuid4(), uuid.uuid4())])
def test_create_role_permission_with_non_existent_parameters(super_user_authenticated_flask_test_client,
                                                             clean_database,
                                                             generate_roles,
                                                             generate_permissions,
                                                             role_id, permission_id):
    request_body = {
        'role_id': role_id,
        'permission_id': permission_id
    }
    response = super_user_authenticated_flask_test_client.post('/api/v1/crud/role_permission/', json=request_body)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.text == ''
