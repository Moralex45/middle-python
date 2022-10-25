import pytest

from tests.functional.testdata.database_fake_data import roles
from http import HTTPStatus


@pytest.mark.parametrize(
    'role',
    [role for role in roles])
def test_get_role_list(
    super_user_authenticated_flask_test_client,
    clean_database,
    generate_roles,
    role
):
    response = super_user_authenticated_flask_test_client.get(f'/api/v1/crud/role/{role["id"]}')
    assert response.status_code == HTTPStatus.OK
    assert response.is_json
    assert response.json == role


def test_get_role_by_id(
    super_user_authenticated_flask_test_client,
    clean_database,
    generate_roles,
):
    role = roles[0]
    response = super_user_authenticated_flask_test_client.get(f'/api/v1/crud/role/{role["id"]}')
    assert response.status_code == HTTPStatus.OK
    assert response.is_json
    assert response.json == role


def test_create_role(
    super_user_authenticated_flask_test_client,
    clean_database,
    generate_roles
):
    request_body = {
        "code": 100,
        "description": "testtest"
    }
    response = super_user_authenticated_flask_test_client.post('/api/v1/crud/role/', json=request_body)
    assert response.status_code == HTTPStatus.OK
    assert response.is_json


def test_update_role_by_id(
    super_user_authenticated_flask_test_client,
    clean_database,
    generate_roles,
):
    request_body = {
        "code": 100,
        "description": "testtest"
    }
    role = roles[0]
    response = super_user_authenticated_flask_test_client.put(f'/api/v1/crud/role/{role["id"]}', json=request_body)
    assert response.status_code == HTTPStatus.OK
    assert response.is_json


def test_delete_role_by_id(
    super_user_authenticated_flask_test_client,
    clean_database,
    generate_roles,
):
    role = roles[0]
    response = super_user_authenticated_flask_test_client.delete(f'/api/v1/crud/role/{role["id"]}')
    assert response.status_code == HTTPStatus.OK
    assert response.is_json
