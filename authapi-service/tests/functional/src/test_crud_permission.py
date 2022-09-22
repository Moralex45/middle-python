import uuid

import pytest

from tests.functional.testdata.database_fake_data import permissions
from http import HTTPStatus

@pytest.mark.parametrize(
    'permission',
    [permission for permission in permissions])
def test_get_permission_list(
    flask_test_client,
    clean_database,
    generate_permissions,
    permission
):
    response = flask_test_client.get(f'/api/v1/crud/permission/{permission["id"]}')
    assert response.status_code == HTTPStatus.OK
    assert response.is_json
    assert response.json == permission

def test_get_role_by_id(
    flask_test_client,
    clean_database,
    generate_permissions,
):
    permission = permissions[0]
    response = flask_test_client.get(f'/api/v1/crud/permission/{permission["id"]}')
    assert response.status_code == HTTPStatus.OK
    assert response.is_json
    assert response.json == permission

def test_create_role(
    flask_test_client,
    clean_database,
    generate_permissions
):
    request_body = {
        "code": 100,
    }
    response = flask_test_client.post(f'/api/v1/crud/permission/', json=request_body)
    assert response.status_code == HTTPStatus.OK
    assert response.is_json

def test_update_role_by_id(
    flask_test_client,
    clean_database,
    generate_permissions,
):
    request_body = {
        "code": 100,
    }
    permission = permissions[0]
    response = flask_test_client.put(f'/api/v1/crud/permission/{permission["id"]}', json=request_body)
    assert response.status_code == HTTPStatus.OK
    assert response.is_json

def test_delete_role_by_id(
    flask_test_client,
    clean_database,
    generate_permissions,
):
    permission = permissions[0]
    response = flask_test_client.delete(f'/api/v1/crud/permission/{permission["id"]}')
    assert response.status_code == HTTPStatus.OK
    assert response.is_json
