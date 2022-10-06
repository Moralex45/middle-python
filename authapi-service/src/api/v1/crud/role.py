import uuid
from http import HTTPStatus

import orjson
from flask import Blueprint, Response, request
from pydantic.json import pydantic_encoder

from src.core.constants import CAN_ACCESS_ROLE
from src.core.in_models.role import Role as InRole
from src.core.out_models.role import Role as OutRole
from src.core.utils import permissions_required, rate_limit
from src.db.services.role import RoleService

blueprint = Blueprint('role', __name__, url_prefix='/api/v1/crud/role')


@blueprint.route('/', methods=['GET'])
@permissions_required(CAN_ACCESS_ROLE['code'])
@rate_limit
def get_role_list():
    response_body = ''
    response_status = HTTPStatus.OK

    db_roles = RoleService.get_all()

    role = orjson.dumps(
        [OutRole.from_orm(db_role) for db_role in db_roles],
        default=pydantic_encoder
    )
    response_body = role

    return Response(response_body, status=response_status, mimetype='application/json')


@blueprint.route('/<uuid:role_id>', methods=['GET'])
@permissions_required(CAN_ACCESS_ROLE['code'])
@rate_limit
def get_role_by_id(role_id: uuid.UUID):
    response_body = ''
    response_status = HTTPStatus.OK

    db_role = RoleService.get_by_id(role_id)
    if db_role is None:
        response_status = HTTPStatus.NO_CONTENT
        return Response(response_body, status=response_status, mimetype='application/json')

    role = OutRole.from_orm(db_role)
    response_body = role.json()

    return Response(response_body, status=response_status, mimetype='application/json')


@blueprint.route('/', methods=['POST'])
@permissions_required(CAN_ACCESS_ROLE['code'])
@rate_limit
def create_role():
    response_body = ''
    response_status = HTTPStatus.OK

    request_body = request.json

    try:
        role_code = request_body.get('code', None)
        role_description = request_body.get('description', None)
        request_role = InRole(code=role_code, description=role_description)
    except (ValueError, AttributeError):
        response_status = HTTPStatus.BAD_REQUEST
        return Response(response_body, status=response_status, mimetype='application/json')

    try:
        db_role = RoleService.create(
            request_role.code,
            request_role.description
        )
        role = OutRole.from_orm(db_role)
        response_body = role.json()

    except ValueError:
        response_status = HTTPStatus.BAD_REQUEST

    return Response(response_body, status=response_status, mimetype='application/json')


@blueprint.route('/<uuid:role_id>', methods=['PUT'])
@permissions_required(CAN_ACCESS_ROLE['code'])
@rate_limit
def change_role(role_id: uuid.UUID):
    response_body = ''
    response_status = HTTPStatus.OK

    request_body = request.json

    try:
        role_code = request_body.get('code', None)
        role_description = request_body.get('description', None)
        request_role = InRole(code=role_code, description=role_description)
    except (ValueError, AttributeError):
        response_status = HTTPStatus.BAD_REQUEST
        return Response(response_body, status=response_status, mimetype='application/json')

    try:
        db_role = RoleService.update(
            role_id,
            request_role.code,
            request_role.description
        )
        role = OutRole.from_orm(db_role)
        response_body = role.json()

    except ValueError:
        response_status = HTTPStatus.BAD_REQUEST

    return Response(response_body, status=response_status, mimetype='application/json')


@blueprint.route('/<uuid:role_id>', methods=['DELETE'])
@permissions_required(CAN_ACCESS_ROLE['code'])
@rate_limit
def delete_role(role_id: uuid.UUID):
    response_body = ''
    response_status = HTTPStatus.OK

    try:
        RoleService.delete_by_id(role_id)
    except ValueError:
        response_status = HTTPStatus.BAD_REQUEST

    return Response(response_body, status=response_status, mimetype='application/json')
