import datetime
from http import HTTPStatus
import secrets

from flask import Blueprint, Response, request, make_response
from flask_jwt_extended import create_access_token

from core.config import get_settings_instance
from core.in_models.user import UserLogin as InUserLogin
from db.services.user import UserService

blueprint = Blueprint('login', __name__, url_prefix='/api/v1/auth/login')


@blueprint.route('/', methods=['POST'])
def login_user():
    response_body = ''
    response_status = HTTPStatus.OK

    request_body = request.json

    try:
        user_name = request_body.get('username', None)
        password = request_body.get('password', None)
        remember = request_body.get('remember', None)
        request_user = InUserLogin(user_name=user_name, password=password, remember=remember)

    except (ValueError, AttributeError):
        response_status = HTTPStatus.UNAUTHORIZED
        return Response(response_body, status=response_status, mimetype='application/json')

    db_user = UserService.get_by_username(request_user.user_name)

    if db_user is None:
        response_status = HTTPStatus.UNAUTHORIZED
        return Response(response_body, status=response_status, mimetype='application/json')

    if not db_user.check_password(password):
        response_status = HTTPStatus.UNAUTHORIZED
        return Response(response_body, status=response_status, mimetype='application/json')

    access_token = create_access_token(identity=db_user)
    response = make_response()
    response.status = response_status
    response.set_cookie(
        key=get_settings_instance().JWT_ACCESS_COOKIE_NAME,
        value=access_token,
        httponly=True,
        expires=datetime.datetime.now() + datetime.timedelta(seconds=get_settings_instance().JWT_ACCESS_TOKEN_EXPIRES)
    )

    refresh_token = secrets.token_hex(32)
    response.set_cookie(
        key=get_settings_instance().REFRESH_TOKEN_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        expires=datetime.datetime.now() + datetime.timedelta(
            days=get_settings_instance().REFRESH_TOKEN_EXPIRES_LONG
            if request_user.remember
            else get_settings_instance().REFRESH_TOKEN_EXPIRES_SHORT)
    )

    pass  # TODO create auth_history entity in db
    pass  # TODO push refresh token in redis

    return response
