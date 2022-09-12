from http import HTTPStatus

from flask import Blueprint

blueprint = Blueprint('role', __name__, url_prefix='/api/v1/role')