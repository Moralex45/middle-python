import datetime
from http import HTTPStatus

import aiohttp as aiohttp
import jwt
from fastapi import HTTPException, Request, Response
from jwt import ExpiredSignatureError, InvalidSignatureError

from src.core.config import get_settings


async def verify_auth_tokens(request: Request, response: Response):
    if get_settings().DEBUG:
        return

    access_token = request.cookies.get(get_settings().JWT_ACCESS_COOKIE_NAME, None)
    refresh_token = request.cookies.get(get_settings().REFRESH_TOKEN_COOKIE_NAME, None)
    if not (access_token is not None and refresh_token is not None):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Unable to fetch required cookies')

    correct_access_token = True

    try:
        jwt.decode(access_token, key=get_settings().JWT_SECRET, algorithms=['HS256'])

    except (InvalidSignatureError, ExpiredSignatureError):
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
        async with session.post(get_settings().AUTH_SERVICE_TOKENS_REFRESH_URL,
                                json=token_refresh_body,
                                headers=headers) as auth_response:
            if auth_response.status != HTTPStatus.OK:
                raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Unable to refresh tokens')

            response_body = await auth_response.json()
            cookie_expires_seconds = (datetime.datetime.fromtimestamp(response_body['refresh_token_expire_timestamp']) -
                                      datetime.datetime.now()).seconds
            response.set_cookie(key=get_settings().JWT_ACCESS_COOKIE_NAME,
                                value=response_body['access_token'],
                                httponly=True,
                                expires=cookie_expires_seconds)
            response.set_cookie(key=get_settings().REFRESH_TOKEN_COOKIE_NAME,
                                value=response_body['refresh_token'],
                                httponly=True,
                                expires=cookie_expires_seconds)
