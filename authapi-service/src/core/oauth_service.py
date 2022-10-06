import datetime
from http import HTTPStatus
import secrets
from src.db.services.user import UserService

from flask_jwt_extended import create_access_token
from flask import make_response

from src.db.services.social_account import SocialAccountService
from src.core.config import get_settings_instance
from src.utils.password_generator import generator_pw


def register_social_account(
    social_name: str,
    social_id: str,
    email: str,
    username: str,
) -> tuple[dict[str, str], int]:

    response_status = HTTPStatus.OK

    current_user = UserService.get_by_username(username=username)

    if not current_user:
        current_user = UserService.create(
            username=username,
            password=generator_pw()
        )

    if not \
        SocialAccountService.\
            get_filtered_by_user_id_and_social_id_and_social_name(
                user_id=current_user.id,
                social_id=social_id,
                social_name=social_name
            ):
        SocialAccountService.create(
            user_id=current_user.id,
            social_id=social_id,
            social_name=social_name
        )

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
