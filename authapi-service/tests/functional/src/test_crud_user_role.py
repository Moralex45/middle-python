import uuid

import pytest

from functional.testdata.database_fake_data import roles_permissions, roles, permissions, users_roles, users
from http import HTTPStatus


@pytest.mark.parametrize(
    'user_role',
    [user_role for user_role in users_roles])
def test_scrap_existing_user_role(flask_test_client, clean_database, generate_users_roles, user_role):
    response = flask_test_client.get(f'/api/v1/user_role/{user_role["id"]}')
    assert response.status_code == HTTPStatus.OK
    assert response.is_json
    assert response.json == user_role


def test_scrap_non_existing_user_role(flask_test_client, clean_database, generate_users_roles):
    response = flask_test_client.get(f'/api/v1/user_role/{uuid.uuid4()}')
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response.text == ''


@pytest.mark.parametrize(
    'user',
    [user for user in users])
def test_scrap_existing_user_role_filtered_by_user_id(flask_test_client,
                                                      clean_database,
                                                      generate_users_roles,
                                                      user):
    response = flask_test_client.get(f'/api/v1/user_role/?user_id={user["id"]}')
    assert response.status_code == HTTPStatus.OK
    assert response.is_json
    assert response.json == list(filter(lambda o: o['user_id'] == user['id'], users_roles))


def test_scrap_non_existing_user_role_permissions_filtered_by_role_id(flask_test_client,
                                                                      clean_database,
                                                                      generate_users_roles):
    response = flask_test_client.get(f'/api/v1/user_role/?user_id={uuid.uuid4()}')
    assert response.status_code == HTTPStatus.OK
    assert response.is_json
    assert response.json == []


def test_scrap_user_role_filtered_by_inappropriate_role_id_format(flask_test_client,
                                                                  clean_database,
                                                                  generate_users_roles):
    response = flask_test_client.get(f'/api/v1/user_role/?user_id={str(uuid.uuid4())[-1:]}')
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.text == ''
