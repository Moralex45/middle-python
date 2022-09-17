import json
from uuid import UUID
from http import HTTPStatus

import orjson
from flask import Blueprint, request, Response
from pydantic.json import pydantic_encoder

from core.out_models.role_permission import RolePermission
from db.services import role_permission_service

blueprint = Blueprint('role_permission', __name__, url_prefix='/api/v1/role_permission')


@blueprint.route('/<uuid:role_permission_id>', methods=['GET'])
def get_role_permission(role_permission_id: UUID):
    response_body = ''
    response_status = HTTPStatus.OK

    db_role_permission = role_permission_service.get_by_id(role_permission_id)
    if db_role_permission is None:
        response_status = HTTPStatus.NO_CONTENT
        return Response(response_body, status=response_status, mimetype='application/json')

    role_permission = RolePermission.from_orm(db_role_permission)
    response_body = role_permission.json()

    return Response(response_body, status=response_status, mimetype='application/json')


@blueprint.route('/', methods=['GET'])
def get_role_permissions():
    response_body = ''
    response_status = HTTPStatus.OK

    role_id: UUID | None = request.args.get('role_id', default=None, type=UUID)
    if role_id is None:
        response_status = HTTPStatus.BAD_REQUEST

        return Response(response_body, status=response_status, mimetype='application/json')

    db_role_permissions = role_permission_service.get_filtered(role_id)
    role_permissions = orjson.dumps(
        [RolePermission.from_orm(db_role_permission) for db_role_permission in db_role_permissions],
        default=pydantic_encoder)
    response_body = role_permissions

    return Response(response_body, status=response_status, mimetype='application/json')
