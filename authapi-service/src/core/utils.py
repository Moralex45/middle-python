import datetime
from functools import wraps
from http import HTTPStatus

from flask import Response, request
from flask_jwt_extended import get_jwt, verify_jwt_in_request

from src import cache
from src.core.config import get_settings_instance


def rate_limit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not get_settings_instance().ENABLE_DDOS_PROTECTION:
            return func(*args, **kwargs)

        current_minute = datetime.datetime.now().minute
        current_request_count = cache.cache_service.get_address_requests_amount(request.remote_addr,
                                                                                current_minute)

        if current_request_count and current_request_count >= get_settings_instance().USER_REQUEST_LIMIT_PER_MINUTE:
            return Response(response='Request limit exceeded',
                            status=HTTPStatus.TOO_MANY_REQUESTS)

        if current_request_count is not None:
            cache.cache_service.increment_address_requests_amount(request.remote_addr, current_minute)

        else:
            cache.cache_service.set_address_requests_amount(request.remote_addr, current_minute, str(1))

        return func(*args, **kwargs)

    return wrapper


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

            return Response(response='Lack of permissions', status=HTTPStatus.FORBIDDEN)

        return decorator

    return wrapper
