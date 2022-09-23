import datetime
import secrets
from http import HTTPStatus

import pytest
from flask import make_response
from flask_jwt_extended import create_access_token

import cache
from db.services.auth_history import AuthHistoryService
from db.services.user import UserService
from functional.testdata.database_fake_data import users, super_users, very_long_access_token, very_long_refresh_token
from src.app_utils import create_raw_app


@pytest.fixture()
def flask_app():
    return create_raw_app()


@pytest.fixture()
def flask_test_client(flask_app, server_settings_instance):
    client = flask_app.test_client()

    return client


@pytest.fixture()
def super_user_authenticated_flask_test_client(flask_test_client,
                                               generate_super_users,
                                               server_settings_instance):

    flask_test_client.set_cookie(
        server_name='127.0.0.1',
        key=server_settings_instance.JWT_ACCESS_COOKIE_NAME,
        value=very_long_access_token,
        httponly=True,
        expires=datetime.datetime.now() + datetime.timedelta(seconds=server_settings_instance.JWT_ACCESS_TOKEN_EXPIRES)
    )

    flask_test_client.set_cookie(
        server_name='127.0.0.1',
        key=server_settings_instance.REFRESH_TOKEN_COOKIE_NAME,
        value=very_long_refresh_token,
        httponly=True,
        expires=datetime.datetime.now() + datetime.timedelta(days=server_settings_instance.REFRESH_TOKEN_EXPIRES_LONG)
    )

    return flask_test_client
