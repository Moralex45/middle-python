import datetime
from http import HTTPStatus

from flask import Blueprint, Response, request
from flask_jwt_extended import current_user

from db.services.user import UserService
from db.services.userdata import UserDataService
from src.core.constants import CAN_EDIT_PROFILE
from src.core.in_models.user import UserUpdate as InUserUpdate
from src.core.utils import permissions_required

blueprint = Blueprint('user', __name__, url_prefix='/api/v1/crud/user')


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
