import datetime
import secrets

import pytest
from flask_jwt_extended import create_access_token

from src.db.services.user import UserService
from tests.functional.testdata.database_fake_data import super_users
from src.app_utils import create_raw_app


@pytest.fixture()
def flask_app():
    app = create_raw_app()
    app.app_context().push()

    return app


@pytest.fixture()
def flask_test_client(flask_app, server_settings_instance):
    client = flask_app.test_client()

    return client


@pytest.fixture()
def super_user_authenticated_flask_test_client(flask_test_client,
                                               clean_database,
                                               generate_super_users,
                                               server_settings_instance):
    db_user = UserService.get_by_username(super_users[0]['username'])

    access_token = create_access_token(identity=db_user)

    refresh_token = secrets.token_hex(32)
    refresh_token_expire_days = server_settings_instance.REFRESH_TOKEN_EXPIRES_LONG
    refresh_token_expire = datetime.datetime.now() + datetime.timedelta(days=refresh_token_expire_days)

    flask_test_client.set_cookie(
        server_name='127.0.0.1',
        key=server_settings_instance.JWT_ACCESS_COOKIE_NAME,
        value=access_token,
        httponly=True,
        expires=datetime.datetime.now() + datetime.timedelta(seconds=server_settings_instance.JWT_ACCESS_TOKEN_EXPIRES)
    )

    flask_test_client.set_cookie(
        server_name='127.0.0.1',
        key=server_settings_instance.REFRESH_TOKEN_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        expires=refresh_token_expire
    )

    return flask_test_client
