import datetime
import secrets
from http import HTTPStatus

from flask import Blueprint, Response, make_response, request
from flask_jwt_extended import create_access_token

from src import cache
from src.core.config import get_settings_instance
from src.core.in_models.user import UserLogin as InUserLogin
from src.core.utils import rate_limit
from src.db.services.auth_history import AuthHistoryService
from src.db.services.user import UserService

blueprint = Blueprint('login', __name__, url_prefix='/api/v1/auth/login')


@blueprint.route('/', methods=['POST'])
@rate_limit
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

    refresh_token = secrets.token_hex(32)
    refresh_token_expire_days = get_settings_instance().REFRESH_TOKEN_EXPIRES_LONG \
        if request_user.remember \
        else get_settings_instance().REFRESH_TOKEN_EXPIRES_SHORT
    refresh_token_expire = datetime.datetime.now() + datetime.timedelta(
        days=refresh_token_expire_days)

    try:
        exist_session = AuthHistoryService.get_by_user_id_and_user_agent(db_user.id, request.user_agent.string)
        if exist_session is not None:
            AuthHistoryService.stop_by_id(exist_session.id)
        AuthHistoryService.create(db_user.id, request.user_agent.string, request.remote_addr)

    except ValueError:
        response_status = HTTPStatus.FORBIDDEN
        return Response(response_body, status=response_status, mimetype='application/json')

    response.status = response_status

    response.set_cookie(
        key=get_settings_instance().JWT_ACCESS_COOKIE_NAME,
        value=access_token,
        httponly=True,
        expires=datetime.datetime.now() + datetime.timedelta(seconds=get_settings_instance().JWT_ACCESS_TOKEN_EXPIRES),
    )

    response.set_cookie(
        key=get_settings_instance().REFRESH_TOKEN_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        expires=refresh_token_expire,
    )

    cache.cache_service.set_user_session_by_user_id_and_user_agent(db_user.id,
                                                                   request.user_agent.string,
                                                                   refresh_token,
                                                                   refresh_token_expire_days * 60 * 60 * 60)

    return response
