import uuid

from functional.testdata.database_fake_data import roles_permissions
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
