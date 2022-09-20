import uuid
from http import HTTPStatus

import orjson
from flask import Blueprint, Response, request
from pydantic.json import pydantic_encoder

from src.core.in_models.role_permission import \
    RolePermission as InRolePermission
from src.core.out_models.role_permission import \
    RolePermission as OutRolePermission
from src.db.services.role_permission import RolePermissionService

blueprint = Blueprint('role_permission', __name__, url_prefix='/api/v1/crud/role_permission')


@blueprint.route('/', methods=['POST'])
def create_role_permission():
    response_body = ''
    response_status = HTTPStatus.OK

    request_body = request.json

    try:
        role_id = uuid.UUID(request_body.get('role_id', None))
        permission_id = uuid.UUID(request_body.get('permission_id', None))
        request_role_permission = InRolePermission(role_id=role_id, permission_id=permission_id)

    except (ValueError, AttributeError):
        response_status = HTTPStatus.BAD_REQUEST
        return Response(response_body, status=response_status, mimetype='application/json')

    try:
        db_role_permission = RolePermissionService.create(request_role_permission.role_id,
                                                          request_role_permission.permission_id)
        role_permission = OutRolePermission.from_orm(db_role_permission)
        response_body = role_permission.json()

    except ValueError:
        response_status = HTTPStatus.BAD_REQUEST

    return Response(response_body, status=response_status, mimetype='application/json')


@blueprint.route('/<uuid:role_permission_id>', methods=['GET'])
def get_role_permission(role_permission_id: uuid.UUID):
    response_body = ''
    response_status = HTTPStatus.OK

    db_role_permission = RolePermissionService.get_by_id(role_permission_id)
    if db_role_permission is None:
        response_status = HTTPStatus.NO_CONTENT
        return Response(response_body, status=response_status, mimetype='application/json')

    role_permission = OutRolePermission.from_orm(db_role_permission)
    response_body = role_permission.json()

    return Response(response_body, status=response_status, mimetype='application/json')


@blueprint.route('/', methods=['GET'])
def get_roles_permissions():
    response_body = ''
    response_status = HTTPStatus.OK

    role_id: uuid.UUID | None = request.args.get('role_id', default=None, type=uuid.UUID)
    if role_id is None:
        response_status = HTTPStatus.BAD_REQUEST

        return Response(response_body, status=response_status, mimetype='application/json')

    db_role_permissions = RolePermissionService.get_filtered(role_id)
    role_permissions = orjson.dumps(
        [OutRolePermission.from_orm(db_role_permission) for db_role_permission in db_role_permissions],
        default=pydantic_encoder)
    response_body = role_permissions

    return Response(response_body, status=response_status, mimetype='application/json')


@blueprint.route('/<uuid:role_permission_id>', methods=['DELETE'])
def delete_role_permission(role_permission_id: uuid.UUID):
    response_body = ''
    response_status = HTTPStatus.OK

    try:
        RolePermissionService.delete_by_id(role_permission_id)

    except ValueError:
        response_status = HTTPStatus.BAD_REQUEST

    return Response(response_body, status=response_status, mimetype='application/json')
