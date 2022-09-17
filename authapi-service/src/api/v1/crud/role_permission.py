import uuid

from flask import Blueprint

from core.out_models.role_permission import RolePermission
from db.services import role_permission_service

blueprint = Blueprint('role_permission', __name__, url_prefix='/api/v1/role_permission')


@blueprint.route('/<uuid:role_permission_id>', methods=('GET',))
def get_role_permission(role_permission_id: uuid):
    db_role_permission = role_permission_service.get_by_id(role_permission_id)
    response_body = ''
    response_code = 200
    if db_role_permission is None:
        response_code = 204
    else:
        role_permission = RolePermission.from_pg(**db_role_permission.__dict__)
        response_body = role_permission.json()

    return response_body, response_code


@blueprint.route('/', methods=('GET',))
def get_role_permissions():
    pass
