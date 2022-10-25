from http import HTTPStatus

from flask import Blueprint, Response, make_response, request
from flask_jwt_extended import current_user, unset_jwt_cookies

from src import cache
from src.core.config import get_settings_instance
from src.core.in_models.auth import Logout
from src.core.utils import permissions_required
from src.db.services.auth_history import AuthHistoryService

blueprint = Blueprint('logout', __name__, url_prefix='/api/v1/auth/logout')


@blueprint.route('/', methods=['POST'])
@permissions_required()
def logout_user():
    response_body = ''
    response_status = HTTPStatus.OK

    request_body = request.json

    try:
        all_devices = request_body.get('all_devices', None)
        logout_data = Logout(all_devices=all_devices)

    except (ValueError, AttributeError):
        response_status = HTTPStatus.UNAUTHORIZED
        return Response(response_body, status=response_status, mimetype='application/json')

    db_user = current_user

    response = make_response()
    response.status_code = response_status
    unset_jwt_cookies(response)
    response.delete_cookie(key=get_settings_instance().REFRESH_TOKEN_COOKIE_NAME,
                           httponly=True)

    if logout_data.all_devices is not None and logout_data.all_devices:
        auth_histories = AuthHistoryService.get_by_user_id(db_user.id)
        for auth_history in auth_histories:
            AuthHistoryService.stop_by_id(auth_history.id)

        cache.cache_service.delete_user_sessions_by_user_id(db_user.id)

    else:
        auth_history = AuthHistoryService.get_by_user_id_and_user_agent(db_user.id, request.user_agent.string)
        if auth_history:
            AuthHistoryService.stop_by_id(auth_history.id)

        cache.cache_service.delete_user_session_by_user_id_and_user_agent(db_user.id, request.user_agent.string)

    return response
