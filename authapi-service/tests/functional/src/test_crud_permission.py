import pytest

from tests.functional.testdata.database_fake_data import permissions
from http import HTTPStatus


@pytest.mark.parametrize(
    'permission',
    [permission for permission in permissions])
def test_get_permission_list(
    super_user_authenticated_flask_test_client,
    clean_database,
    generate_permissions,
    permission
):
    response = super_user_authenticated_flask_test_client.get(f'/api/v1/crud/permission/{permission["id"]}')
    assert response.status_code == HTTPStatus.OK
    assert response.is_json
    assert response.json == permission


def test_get_role_by_id(
    super_user_authenticated_flask_test_client,
    clean_database,
    generate_permissions,
):
    permission = permissions[0]
    response = super_user_authenticated_flask_test_client.get(f'/api/v1/crud/permission/{permission["id"]}')
    assert response.status_code == HTTPStatus.OK
    assert response.is_json
    assert response.json == permission


def test_create_role(
    super_user_authenticated_flask_test_client,
    clean_database,
    generate_permissions
):
    request_body = {
        "code": 100,
    }
    response = super_user_authenticated_flask_test_client.post('/api/v1/crud/permission/', json=request_body)
    assert response.status_code == HTTPStatus.OK
    assert response.is_json


def test_update_role_by_id(
    super_user_authenticated_flask_test_client,
    clean_database,
    generate_permissions,
):
    request_body = {
        "code": 100,
    }
    permission = permissions[0]
    response = super_user_authenticated_flask_test_client.put(
        f'/api/v1/crud/permission/{permission["id"]}', json=request_body
    )
    assert response.status_code == HTTPStatus.OK
    assert response.is_json


def test_delete_role_by_id(
    super_user_authenticated_flask_test_client,
    clean_database,
    generate_permissions,
):
    permission = permissions[0]
    response = super_user_authenticated_flask_test_client.delete(f'/api/v1/crud/permission/{permission["id"]}')
    assert response.status_code == HTTPStatus.OK
    assert response.is_json
