import uuid
from http import HTTPStatus

from flask import Blueprint, Response, request
import orjson
from pydantic.json import pydantic_encoder

from db.services.user_role import UserRoleService
from core.out_models.user_role import UserRole as OutUserRole

blueprint = Blueprint('user_role', __name__, url_prefix='/api/v1/user_role')


@blueprint.route('/<uuid:user_role_id>', methods=['GET'])
def get_role_permission(user_role_id: uuid.UUID):
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
def get_roles_permissions():
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
