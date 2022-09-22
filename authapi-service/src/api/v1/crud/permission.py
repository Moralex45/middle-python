import uuid
from http import HTTPStatus

import orjson
from flask import Blueprint, Response, request
from pydantic.json import pydantic_encoder

from src.core.in_models.permission import Permission as InPermission
from src.core.out_models.permission import Permission as OutPermission
from src.db.services.permissions import PermissionService

blueprint = Blueprint('permission', __name__, url_prefix='/api/v1/crud/permission')


@blueprint.route('/', methods=['GET'])
def get_permission_list():
    response_body = ''
    response_status = HTTPStatus.OK

    db_permissions = PermissionService.get_all()

    permission = orjson.dumps(
        [OutPermission.from_orm(db_permission) for db_permission in db_permissions],
        default=pydantic_encoder
    )
    response_body = permission

    return Response(response_body, status=response_status, mimetype='application/json')


@blueprint.route('/<uuid:permission_id>', methods=['GET'])
def get_permission_by_id(permission_id: uuid.UUID):
    response_body = ''
    response_status = HTTPStatus.OK

    db_permission = PermissionService.get_by_id(permission_id)
    if db_permission is None:
        response_status = HTTPStatus.NO_CONTENT
        return Response(response_body, status=response_status, mimetype='application/json')

    permission = OutPermission.from_orm(db_permission)
    response_body = permission.json()

    return Response(response_body, status=response_status, mimetype='application/json')


@blueprint.route('/', methods=['POST'])
def create_permission():
    response_body = ''
    response_status = HTTPStatus.OK

    request_body = request.json

    try:
        role_code = request_body.get('code', None)
        request_permission = InPermission(code=role_code)
    except (ValueError, AttributeError):
        response_status = HTTPStatus.BAD_REQUEST
        return Response(response_body, status=response_status, mimetype='application/json')

    try:
        db_permission = PermissionService.create(
            request_permission.code
        )

        permission = OutPermission.from_orm(db_permission)
        response_body = permission.json()

    except ValueError:
        response_status = HTTPStatus.BAD_REQUEST

    return Response(response_body, status=response_status, mimetype='application/json')


@blueprint.route('/<uuid:permission_id>', methods=['PUT'])
def change_role(permission_id: uuid.UUID):
    response_body = ''
    response_status = HTTPStatus.OK

    request_body = request.json

    try:
        role_code = request_body.get('code', None)
        request_permission = InPermission(code=role_code)
    except (ValueError, AttributeError):
        response_status = HTTPStatus.BAD_REQUEST
        return Response(response_body, status=response_status, mimetype='application/json')

    try:
        db_permission = PermissionService.update(
            permission_id,
            request_permission.code
        )
        permission = OutPermission.from_orm(db_permission)
        response_body = permission.json()

    except ValueError:
        response_status = HTTPStatus.BAD_REQUEST

    return Response(response_body, status=response_status, mimetype='application/json')


@blueprint.route('/<uuid:permission_id>', methods=['DELETE'])
def delete_role(permission_id: uuid.UUID):
    response_body = ''
    response_status = HTTPStatus.OK

    try:
        PermissionService.delete_by_id(permission_id)
    except ValueError:
        response_status = HTTPStatus.BAD_REQUEST

    return Response(response_body, status=response_status, mimetype='application/json')
