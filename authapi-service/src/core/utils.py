from functools import wraps
from http import HTTPStatus

from flask import Response
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def permissions_required(*permissions):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            is_super = claims['is_super']
            user_permissions = claims['permissions']
            access_allowed = True

            for permission in permissions:
                if permission not in user_permissions:
                    access_allowed = False

            if is_super or access_allowed:
                return fn(*args, **kwargs)
            else:
                return Response(response='Lack of permissions', status=HTTPStatus.FORBIDDEN)

        return decorator

    return wrapper
