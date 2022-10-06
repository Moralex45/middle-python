import datetime
import uuid
from http import HTTPStatus

import orjson
from flask import Blueprint, Response, request
from flask_jwt_extended import current_user
from pydantic.json import pydantic_encoder

from src.core.constants import CAN_EDIT_PROFILE
from src.core.in_models.user import UserUpdate as InUserUpdate
from src.core.out_models.user import CheckUserPermissions, UserLoginHistory
from src.core.utils import permissions_required, rate_limit
from src.db.services.auth_history import AuthHistoryService
from src.db.services.user import UserService
from src.db.services.userdata import UserDataService

blueprint = Blueprint('user', __name__, url_prefix='/api/v1/crud/user')


@blueprint.route('/<uuid:user_id>/check_permissions', methods=['POST'])
def check_permissions(user_id: uuid.UUID):
    """
    Accepts url request like this:
    /api/v1/crud/user/user_id:uuid/check_permissions?permission=1000&permission=1001&permission=1002

    """
    response_body = ''
    response_status = HTTPStatus.OK
    required_permissions = [int(required_permission) for required_permission in request.args.getlist('permission')]

    if not len(required_permissions):
        response_status = HTTPStatus.BAD_REQUEST
        return Response(response_body, status=response_status, mimetype='application/json')

    result = UserService.check_permissions(user_id, required_permissions)
    response_obj = CheckUserPermissions(result=result)
    response_body = response_obj.json()

    return Response(response_body, status=response_status, mimetype='application/json')


@blueprint.route('/login_history', methods=['GET'])
@permissions_required()
def login_history():
    response_body = ''
    response_status = HTTPStatus.OK

    db_user = current_user

    db_user_auth_history = AuthHistoryService.get_by_user_id(db_user.id)

    db_user_auth_history = [UserLoginHistory.from_orm(login_session) for login_session in db_user_auth_history]
    user_auth_history = orjson.dumps(db_user_auth_history, default=pydantic_encoder)

    response_body = user_auth_history

    return Response(response_body, status=response_status, mimetype='application/json')


@blueprint.route('/', methods=['POST'])
@permissions_required(CAN_EDIT_PROFILE['code'])
def update_credentials():
    response_body = ''
    response_status = HTTPStatus.OK

    request_body = request.json

    try:
        password = request_body.get('password', None)
        new_password = request_body.get('new_password', None)
        user_name = request_body.get('user_name', None)
        first_name = request_body.get('first_name', None)
        last_name = request_body.get('last_name', None)
        email = request_body.get('email', None)
        birth_date = request_body.get('birth_date', None)
        user_update = InUserUpdate(password=password,
                                   new_password=new_password,
                                   user_name=user_name,
                                   first_name=first_name,
                                   last_name=last_name,
                                   email=email,
                                   birth_date=birth_date)
    except (ValueError, AttributeError):
        response_status = HTTPStatus.BAD_REQUEST
        return Response(response_body, status=response_status, mimetype='application/json')

    db_user = current_user
    if not db_user.check_password(password):
        response_status = HTTPStatus.FORBIDDEN
        return Response(response_body, status=response_status, mimetype='application/json')

    if user_update.user_name is not None or user_update.password is not None:
        UserService.update(_id=db_user.id, username=user_update.user_name, password=user_update.new_password)

    if user_update.first_name is not None \
            or user_update.last_name is not None \
            or user_update.email is not None \
            or user_update.birth_date is not None:
        if user_update.birth_date is not None:
            try:
                birth_date = datetime.datetime.fromtimestamp(birth_date)
            except Exception:
                response_status = HTTPStatus.BAD_REQUEST
                return Response(response_body, status=response_status, mimetype='application/json')

        UserDataService.update(user_id=db_user.id, first_name=user_update.first_name, last_name=user_update.last_name,
                               email=user_update.email, birth_date=birth_date)

    return Response(response_body, status=response_status, mimetype='application/json')
