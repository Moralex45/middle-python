import datetime
import http

import aiohttp
import fastapi
import jwt

import src.core.config as project_config


async def verify_auth_tokens(request: fastapi.Request, response: fastapi.Response):
    if project_config.get_settings().debug:
        return

    access_token = request.cookies.get(project_config.get_settings().jwt_access_cookie_name, None)
    refresh_token = request.cookies.get(project_config.get_settings().refresh_token_cookie_name, None)
    if not (access_token is not None and refresh_token is not None):
        raise fastapi.HTTPException(status_code=http.HTTPStatus.UNAUTHORIZED, detail='Unable to fetch required cookies')

    correct_access_token = True

    try:
        jwt.decode(access_token, key=project_config.get_settings().jwt_secret, algorithms=['HS256'])

    except (jwt.InvalidSignatureError, jwt.ExpiredSignatureError):
        correct_access_token = False

    if correct_access_token:
        return

    token_refresh_body = {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user_agent': request.headers.get('user-agent'),
    }

    headers = {'user-agent': request.headers.get('user-agent')}

    async with aiohttp.ClientSession() as session:
        async with session.post(project_config.get_settings().auth_service_tokens_refresh_url,
                                json=token_refresh_body,
                                headers=headers) as auth_response:
            if auth_response.status != http.HTTPStatus.OK:
                raise fastapi.HTTPException(status_code=http.HTTPStatus.UNAUTHORIZED, detail='Unable to refresh tokens')

            response_body = await auth_response.json()
            cookie_expires_seconds = (datetime.datetime.fromtimestamp(response_body['refresh_token_expire_timestamp']) -
                                      datetime.datetime.now()).seconds
            response.set_cookie(key=project_config.get_settings().jwt_access_cookie_name,
                                value=response_body['access_token'],
                                httponly=True,
                                expires=cookie_expires_seconds)
            response.set_cookie(key=project_config.get_settings().refresh_token_cookie_name,
                                value=response_body['refresh_token'],
                                httponly=True,
                                expires=cookie_expires_seconds)
