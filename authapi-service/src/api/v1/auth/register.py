from http import HTTPStatus

from flask import Blueprint, Response, request

from core.utils import rate_limit
from src.core.constants import SAMPLE_USER_ROLE
from src.core.in_models.user import UserRegister as InUserRegister
from src.db.services.role import RoleService
from src.db.services.user import UserService
from src.db.services.user_role import UserRoleService
from src.db.services.userdata import UserDataService

blueprint = Blueprint('register', __name__, url_prefix='/api/v1/auth/register')


@blueprint.route('/', methods=['POST'])
@rate_limit
def register_user():
    response_body = ''
    response_status = HTTPStatus.OK

    request_body = request.json

    try:
        user_name = request_body.get('username', None)
        password = request_body.get('password', None)
        request_user = InUserRegister(user_name=user_name, password=password)

    except (ValueError, AttributeError):
        response_status = HTTPStatus.BAD_REQUEST
        return Response(response_body, status=response_status, mimetype='application/json')

    try:
        db_user = UserService.create(request_user.user_name, request_user.password)
        UserDataService.create(db_user.id)
        UserRoleService.create(db_user.id, RoleService.get_by_code(SAMPLE_USER_ROLE['code']).id)

    except ValueError:
        response_status = HTTPStatus.BAD_REQUEST

    return Response(response_body, status=response_status, mimetype='application/json')
