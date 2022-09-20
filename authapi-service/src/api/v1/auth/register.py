from http import HTTPStatus

from flask import Blueprint, request, Response

from core.in_models.user import UserRegister as InUserRegister
from db.services.user import UserService
from db.services.userdata import UserDataService

blueprint = Blueprint('register', __name__, url_prefix='/api/v1/auth/register')


@blueprint.route('/', methods=['POST'])
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

    except ValueError:
        response_status = HTTPStatus.BAD_REQUEST

    return Response(response_body, status=response_status, mimetype='application/json')
