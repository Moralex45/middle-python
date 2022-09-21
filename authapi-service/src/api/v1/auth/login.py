from http import HTTPStatus

from flask import Blueprint, Response, request

from core.in_models.user import UserLogin as InUserLogin
from db.services.user import UserService
from db.services.userdata import UserDataService

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

    pass  # TODO create access token
    pass  # TODO create refresh token
    pass  # TODO Set refresh token in http only cookie
    pass  # TODO create auth_history entity in db
    pass  # TODO push refresh token in redis

    return Response(response_body, status=response_status, mimetype='application/json')
