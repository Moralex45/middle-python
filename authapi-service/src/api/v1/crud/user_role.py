import uuid
from http import HTTPStatus

import orjson
from flask import Blueprint, Response, request
from pydantic.json import pydantic_encoder

from src.core.constants import CAN_ACCESS_USER_ROLE
from src.core.in_models.user_role import UserRole as InUserRole
from src.core.out_models.user_role import UserRole as OutUserRole
from src.core.utils import permissions_required, rate_limit
from src.db.services.user_role import UserRoleService

blueprint = Blueprint('user_role', __name__, url_prefix='/api/v1/crud/user_role')


@blueprint.route('/', methods=['POST'])
@permissions_required(CAN_ACCESS_USER_ROLE['code'])
@rate_limit
def create_user_role():
    response_body = ''
    response_status = HTTPStatus.OK

    request_body = request.json

    try:
        user_id = uuid.UUID(request_body.get('user_id', None))
        role_id = uuid.UUID(request_body.get('role_id', None))
        request_user_role = InUserRole(user_id=user_id, role_id=role_id)

    except (ValueError, AttributeError):
        response_status = HTTPStatus.BAD_REQUEST
        return Response(response_body, status=response_status, mimetype='application/json')

    try:
        db_user_role = UserRoleService.create(request_user_role.user_id,
                                              request_user_role.role_id)
        user_role = OutUserRole.from_orm(db_user_role)
        response_body = user_role.json()

    except ValueError:
        response_status = HTTPStatus.BAD_REQUEST

    return Response(response_body, status=response_status, mimetype='application/json')


@blueprint.route('/<uuid:user_role_id>', methods=['GET'])
@permissions_required(CAN_ACCESS_USER_ROLE['code'])
@rate_limit
def get_user_role(user_role_id: uuid.UUID):
    response_body = ''
    response_status = HTTPStatus.OK

    db_user_role = UserRoleService.get_by_id(user_role_id)
    if db_user_role is None:
        response_status = HTTPStatus.NO_CONTENT
        return Response(response_body, status=response_status, mimetype='application/json')

    user_role = OutUserRole.from_orm(db_user_role)
    response_body = user_role.json()

    return Response(response_body, status=response_status, mimetype='application/json')


@blueprint.route('/', methods=['GET'])
@permissions_required(CAN_ACCESS_USER_ROLE['code'])
@rate_limit
def get_filtered_users_roles_by_user_id():
    response_body = ''
    response_status = HTTPStatus.OK

    user_id: uuid.UUID | None = request.args.get('user_id', default=None, type=uuid.UUID)
    if user_id is None:
        response_status = HTTPStatus.BAD_REQUEST

        return Response(response_body, status=response_status, mimetype='application/json')

    db_users_roles = UserRoleService.get_filtered(user_id)
    role_permissions = orjson.dumps(
        [OutUserRole.from_orm(db_user_role) for db_user_role in db_users_roles],
        default=pydantic_encoder)
    response_body = role_permissions

    return Response(response_body, status=response_status, mimetype='application/json')


@blueprint.route('/<uuid:user_role_id>', methods=['DELETE'])
@permissions_required(CAN_ACCESS_USER_ROLE['code'])
@rate_limit
def delete_user_role(user_role_id: uuid.UUID):
    response_body = ''
    response_status = HTTPStatus.OK

    try:
        UserRoleService.delete_by_id(user_role_id)

    except ValueError:
        response_status = HTTPStatus.BAD_REQUEST

    return Response(response_body, status=response_status, mimetype='application/json')
