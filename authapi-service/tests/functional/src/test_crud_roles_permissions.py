import uuid

from functional.testdata.database_fake_data import roles_permissions, roles
from http import HTTPStatus


def test_scrap_existing_roles_permissions(flask_test_client, clean_database, generate_roles_permissions):
    role_permission = roles_permissions[0]
    response = flask_test_client.get(f'/api/v1/role_permission/{role_permission["id"]}')
    assert response.status_code == HTTPStatus.OK
    assert response.json == role_permission


def test_scrap_non_existing_roles_permissions(flask_test_client, clean_database, generate_roles_permissions):
    response = flask_test_client.get(f'/api/v1/role_permission/{uuid.uuid4()}')
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response.text == ''


def test_scrap_existing_roles_permissions_filtered_by_role_id(flask_test_client,
                                                              clean_database,
                                                              generate_roles_permissions):
    role = roles[0]
    response = flask_test_client.get(f'/api/v1/role_permission/?role_id={role["id"]}')
    assert response.status_code == HTTPStatus.OK
    assert response.json == list(filter(lambda o: o['role_id'] == role['id'], roles_permissions))


def test_scrap_non_existing_roles_permissions_filtered_by_role_id(flask_test_client,
                                                                  clean_database,
                                                                  generate_roles_permissions):
    response = flask_test_client.get(f'/api/v1/role_permission/?role_id={uuid.uuid4()}')
    assert response.status_code == HTTPStatus.OK
    assert response.json == []


def test_scrap_roles_permissions_filtered_by_inappropriate_role_id_format(flask_test_client,
                                                                          clean_database,
                                                                          generate_roles_permissions):
    response = flask_test_client.get(f'/api/v1/role_permission/?role_id={str(uuid.uuid4())[-1:]}')
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.text == ''


def test_delete_existing_roles_permissions(flask_test_client, clean_database, generate_roles_permissions):
    role_permission = roles_permissions[0]
    response = flask_test_client.delete(f'/api/v1/role_permission/{role_permission["id"]}')
    assert response.status_code == HTTPStatus.OK
    assert response.text == ''

    response = flask_test_client.get(f'/api/v1/role_permission/{role_permission["id"]}')
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response.text == ''


def test_delete_non_existing_roles_permissions(flask_test_client, clean_database, generate_roles_permissions):
    response = flask_test_client.delete(f'/api/v1/role_permission/{uuid.uuid4()}')
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.text == ''
