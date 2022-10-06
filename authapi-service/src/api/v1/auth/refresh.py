import datetime
import secrets
from http import HTTPStatus

import jwt
from flask import Blueprint, Response, make_response, request
from flask_jwt_extended import create_access_token

from src import cache
from src.core.config import get_settings_instance
from src.core.in_models.auth import RefreshSession
from src.core.out_models.auth import SuccessfulLogin
from src.db.services.auth_history import AuthHistoryService
from src.db.services.user import UserService

blueprint = Blueprint('refresh', __name__, url_prefix='/api/v1/auth/refresh')


@blueprint.route('/body', methods=['POST'])
def body_refresh():
    response_body = ''
    response_status = HTTPStatus.OK

    request_body = request.json

    try:
        access_token = request_body.get('access_token', None)
        refresh_token = request_body.get('refresh_token', None)
        user_agent = request_body.get('user_agent', None)
        request_session = RefreshSession(access_token=access_token, refresh_token=refresh_token, user_agent=user_agent)

    except (ValueError, AttributeError):
        response_status = HTTPStatus.UNAUTHORIZED
        return Response(response_body, status=response_status, mimetype='application/json')

    try:
        jwt_decoded_data = jwt.decode(request_session.access_token,
                                      get_settings_instance().JWT_SECRET_KEY,
                                      algorithms='HS256',
                                      options={'verify_signature': False})

    except Exception:
        return Response('Login required', status=HTTPStatus.UNAUTHORIZED, mimetype='application/text')

    user_id = jwt_decoded_data['sub']

    session = cache.cache_service.get_user_session_by_user_id_and_user_agent(user_id, request.user_agent.string)
    if session is None:
        return Response('Login required', status=HTTPStatus.UNAUTHORIZED, mimetype='application/text')

    db_user = UserService.get_by_id(user_id)
    if db_user is None:
        return Response('Login required', status=HTTPStatus.UNAUTHORIZED, mimetype='application/text')

    cache.cache_service.delete_user_session_by_user_id_and_user_agent(user_id, request.user_agent.string)
    AuthHistoryService.refresh_by_user_id_and_user_agent(user_id, request.user_agent.string)

    access_token = create_access_token(identity=db_user)

    refresh_token = secrets.token_hex(32)
    refresh_token_expire_days = get_settings_instance().REFRESH_TOKEN_EXPIRES_LONG
    refresh_token_expire = int((datetime.datetime.now() + datetime.timedelta(
        days=refresh_token_expire_days)).timestamp())
    access_token_expire = int((datetime.datetime.now() + datetime.timedelta(
        seconds=get_settings_instance().JWT_ACCESS_TOKEN_EXPIRES)).timestamp())

    login_session = SuccessfulLogin(access_token=access_token,
                                    refresh_token=refresh_token,
                                    access_token_expire_timestamp=access_token_expire,
                                    refresh_token_expire_timestamp=refresh_token_expire)

    cache.cache_service.set_user_session_by_user_id_and_user_agent(db_user.id,
                                                                   request.user_agent.string,
                                                                   refresh_token,
                                                                   refresh_token_expire_days * 60 * 60 * 60)

    response_body = login_session.json()

    return Response(response_body, status=response_status, mimetype='application/json')


@blueprint.route('/', methods=['POST'])
def cookie_refresh():
    access_token = request.cookies.get(get_settings_instance().JWT_ACCESS_COOKIE_NAME)
    if access_token is None:
        return Response('Login required', status=HTTPStatus.UNAUTHORIZED, mimetype='application/text')

    try:
        jwt_decoded_data = jwt.decode(access_token,
                                      get_settings_instance().JWT_SECRET_KEY,
                                      algorithms='HS256',
                                      options={'verify_signature': False})

    except Exception:
        return Response('Login required', status=HTTPStatus.UNAUTHORIZED, mimetype='application/text')

    user_id = jwt_decoded_data['sub']

    session = cache.cache_service.get_user_session_by_user_id_and_user_agent(user_id, request.user_agent.string)
    if session is None:
        return Response('Login required', status=HTTPStatus.UNAUTHORIZED, mimetype='application/text')

    db_user = UserService.get_by_id(user_id)
    if db_user is None:
        return Response('Login required', status=HTTPStatus.UNAUTHORIZED, mimetype='application/text')

    response = make_response()
    response.status = HTTPStatus.OK

    cache.cache_service.delete_user_session_by_user_id_and_user_agent(user_id, request.user_agent.string)
    AuthHistoryService.refresh_by_user_id_and_user_agent(user_id, request.user_agent.string)

    access_token = create_access_token(identity=db_user)

    refresh_token = secrets.token_hex(32)
    refresh_token_expire_days = get_settings_instance().REFRESH_TOKEN_EXPIRES_LONG
    refresh_token_expire = datetime.datetime.now() + datetime.timedelta(days=refresh_token_expire_days)

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

    cache.cache_service.set_user_session_by_user_id_and_user_agent(db_user.id,
                                                                   request.user_agent.string,
                                                                   refresh_token,
                                                                   refresh_token_expire_days * 60 * 60 * 60)

    return response
