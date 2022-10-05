import datetime
from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, Type

import aiohttp
import orjson
import jwt
from http import HTTPStatus
from fastapi import Request, HTTPException, Response
from pydantic import parse_obj_as
from pydantic.json import pydantic_encoder

from core.config import get_settings_instance
from models.base import Base


async def verify_token(request: Request, response: Response):
    access_token = request.cookies.get(get_settings_instance().JWT_ACCESS_COOKIE_NAME, None)
    refresh_token = request.cookies.get(get_settings_instance().REFRESH_TOKEN_COOKIE_NAME, None)
    if not (access_token is not None and refresh_token is not None):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Unable to fetch required cookies')

    encoded_jwt_claims = jwt.decode(access_token, options={'verify_signature': False})
    if datetime.datetime.now().timestamp() < encoded_jwt_claims['exp']:
        return

    token_refresh_body = {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user_agent': request.headers.get('user-agent')
    }

    headers = {'user-agent': request.headers.get('user-agent')}

    async with aiohttp.ClientSession() as session:
        async with session.post(get_settings_instance().AUTH_SERVICE_TOKENS_REFRESH_URL,
                                json=token_refresh_body,
                                headers=headers) as auth_response:
            if auth_response.status != HTTPStatus.OK:
                raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Unable to refresh tokens')

            response_body = await auth_response.json()
            cookie_expires_seconds = (datetime.datetime.fromtimestamp(response_body['access_token_expire_timestamp']) -
                                      datetime.datetime.now()).seconds
            response.set_cookie(key=get_settings_instance().JWT_ACCESS_COOKIE_NAME,
                                value=response_body['access_token'],
                                httponly=True,
                                expires=cookie_expires_seconds)
            cookie_expires_seconds = (datetime.datetime.fromtimestamp(response_body['refresh_token_expire_timestamp']) -
                                      datetime.datetime.now()).seconds
            response.set_cookie(key=get_settings_instance().REFRESH_TOKEN_COOKIE_NAME,
                                value=response_body['refresh_token'],
                                httponly=True,
                                expires=cookie_expires_seconds)


class Serializer(ABC):
    @staticmethod
    @abstractmethod
    def serialize(obj: Any) -> str:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def deserialize(data: str, base_class: Type) -> Any:
        raise NotImplementedError()


class PydanticModelSerializer(Serializer):
    @staticmethod
    def serialize(obj: Base) -> str:
        return obj.json()

    @staticmethod
    def deserialize(data: str, base_class: Type[Base]) -> Any:
        base_class.parse_raw(data)


class PydanticModelListSerializer(Serializer):
    @staticmethod
    def serialize(obj: list[Base]) -> str:
        return orjson.dumps(obj, default=pydantic_encoder).decode()

    @staticmethod
    def deserialize(data: str, base_class: Type[Base]) -> Any:
        parse_obj_as(list[base_class], orjson.loads(data))
