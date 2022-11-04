from __future__ import annotations

import uuid

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
             description='Создание новой оценки кинопроизведения в системе',
             summary='Endpoint позволяет создать новую оценку кинопроизведения в системе',
             tags=['Лайки'],
             dependencies=[fastapi.Depends(verify_auth_tokens)])
async def create_like(
        http_like: http_likes_models.Like,
        like_repository: AsyncMongoDBLikeRepository = fastapi.Depends(get_like_repository),
) -> inner_likes_models.Like:
    try:
        return await like_repository.create_like(
            http_like.user_id, http_like.movie_id, http_like.mark, http_like.device_fingerprint,
        )

    except repositories_exception.DataAlreadyExistsError:
        raise fastapi.HTTPException(status_code=400, detail='Like already exist')


@router.delete('/',
               status_code=fastapi.status.HTTP_200_OK,
               description='Удаление оценки кинопроизведения в системе',
               summary='Endpoint позволяет удалить оценку кинопроизведения в системе',
               tags=['Лайки'],
               dependencies=[fastapi.Depends(verify_auth_tokens)])
async def delete_like(
        user_id: uuid.UUID, movie_id: uuid.UUID,
        like_repository: AsyncMongoDBLikeRepository = fastapi.Depends(get_like_repository),
) -> None:
    try:
        await like_repository.delete_like(user_id, movie_id)

    except repositories_exception.DataDoesNotExistError:
        raise fastapi.HTTPException(status_code=400, detail='Like does not exist')


@router.patch('/',
              response_model=inner_likes_models.Like,
              status_code=fastapi.status.HTTP_200_OK,
              description='Изменение оценки кинопроизведения в системе',
              summary='Endpoint позволяет изменить оценку кинопроизведения в системе',
              tags=['Лайки'],
              dependencies=[fastapi.Depends(verify_auth_tokens)])
async def update_like(
        user_id: uuid.UUID, movie_id: uuid.UUID, mark: int,
        like_repository: AsyncMongoDBLikeRepository = fastapi.Depends(get_like_repository),
) -> inner_likes_models.Like:
    like = await like_repository.get_like(user_id, movie_id)
    if like is None:
        raise fastapi.HTTPException(status_code=400, detail='Like does not exist')
    await like_repository.delete_like(user_id, movie_id)
    return await like_repository.create_like(like.user_id, like.movie_id, mark, like.device_fingerprint, _id=like.id)
