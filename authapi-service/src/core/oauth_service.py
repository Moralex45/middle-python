import datetime
from http import HTTPStatus
import secrets
from src.db.services.user import UserService
from src.db.models.social_account import SocialAccount

from flask_jwt_extended import create_access_token
from flask import make_response
from src.core.config import get_settings_instance


def register_social_account(
    social_name: str,
    social_id: str,
    email: str,
    username: str,
    request: None,
) -> tuple[dict[str, str], int]:

    response_status = HTTPStatus.OK

    current_user = UserService.get_by_username(username=username)

    if not current_user:
        current_user = UserService.create(
            username=username,
            password="Qwerty123"
        )

    if not SocialAccount.raw_exists(
        user_id=current_user.id, social_id=social_id, social_name=social_name
    ):
        SocialAccount(
            user_id=current_user.id, social_id=social_id, social_name=social_name
        ).save_to_db()

    access_token = create_access_token(identity=current_user)
    response = make_response()

    refresh_token = secrets.token_hex(32)
    refresh_token_expire_days = get_settings_instance().REFRESH_TOKEN_EXPIRES_SHORT
    refresh_token_expire = datetime.datetime.now() + datetime.timedelta(
        days=refresh_token_expire_days)

    response.status = response_status
    response.set_cookie(
        key=get_settings_instance().JWT_ACCESS_COOKIE_NAME,
        value=access_token,
        httponly=True,
        expires=datetime.datetime.now() + datetime.timedelta(seconds=get_settings_instance().JWT_ACCESS_TOKEN_EXPIRES)
    )

    response.set_cookie(
        key=get_settings_instance().REFRESH_TOKEN_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        expires=refresh_token_expire
    )

    return response
