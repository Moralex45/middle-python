from __future__ import annotations
import uuid
from contextlib import suppress

import fastapi

from src.core.utils import verify_auth_tokens
import src.models.http.events.like as http_likes_models
import src.models.inner.events.like as inner_likes_models
import src.core.exceptions.repositories as repositories_exception
from src.repositories.like import AsyncMongoDBLikeRepository, get_like_repository

router = fastapi.APIRouter(prefix='/api/v1/likes')


@router.post('/',
             response_model=inner_likes_models.Like,
             status_code=fastapi.status.HTTP_201_CREATED,
             description='Создание нового лайка в системе',
             summary='Endpoint позволяет создать новый лайк в системе',
             tags=['Лайки'],
             dependencies=[fastapi.Depends(verify_auth_tokens)])
async def create_like(
        http_like: http_likes_models.Like,
        like_repository: AsyncMongoDBLikeRepository = fastapi.Depends(get_like_repository),
) -> inner_likes_models.Like:
    try:
        return await like_repository.create_like(http_like.user_id, http_like.movie_id, http_like.device_fingerprint)

    except repositories_exception.DataAlreadyExistsError:
        raise fastapi.HTTPException(status_code=400, detail='Like already exist')

