from __future__ import annotations

import uuid
from typing import List

import fastapi

import src.core.exceptions.repositories as repositories_exception
import src.models.http.events.bookmark as http_bookmarks_models
from src.core.utils import verify_auth_tokens
from src.repositories.bookmark import (AsyncMongoDBBookmarkRepository,
                                       get_bookmark_repository)

router = fastapi.APIRouter(prefix='/api/v1/bookmarks')


@router.post('/',
             response_model=http_bookmarks_models.Bookmark,
             status_code=fastapi.status.HTTP_201_CREATED,
             description='Создание новой закладки пользователя в системе',
             summary='Endpoint позволяет создать новую закладу пользователя в системе',
             tags=['Закладки'],
             dependencies=[fastapi.Depends(verify_auth_tokens)])
async def create_bookmark(
        http_bookmark: http_bookmarks_models.BookmarkCreation,
        bookmark_repository: AsyncMongoDBBookmarkRepository = fastapi.Depends(get_bookmark_repository),
) -> http_bookmarks_models.Bookmark:
    try:
        bookmark = await bookmark_repository.create_bookmark(
            http_bookmark.user_id, http_bookmark.movie_id,
        )
        return http_bookmarks_models.Bookmark(**bookmark.to_dict(False))

    except repositories_exception.DataAlreadyExistsError:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_400_BAD_REQUEST, detail='Bookmark already exist')


@router.delete('/',
               status_code=fastapi.status.HTTP_200_OK,
               description='Удаление закладки пользователя в системе',
               summary='Endpoint позволяет удалить закладку пользователя в системе',
               tags=['Закладки'],
               dependencies=[fastapi.Depends(verify_auth_tokens)])
async def delete_bookmark(
        user_id: uuid.UUID, movie_id: uuid.UUID,
        bookmark_repository: AsyncMongoDBBookmarkRepository = fastapi.Depends(get_bookmark_repository),
) -> None:
    try:
        await bookmark_repository.delete_bookmark(user_id, movie_id)

    except repositories_exception.DataDoesNotExistError:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_400_BAD_REQUEST, detail='Bookmark does not exist')


@router.get('/',
            response_model=List[http_bookmarks_models.Bookmark],
            status_code=fastapi.status.HTTP_200_OK,
            description='Получение закладок пользователя в системе',
            summary='Endpoint позволяет получить закладки пользователя в системе',
            tags=['Закладки'],
            dependencies=[fastapi.Depends(verify_auth_tokens)])
async def get_user_bookmarks(
        user_id: uuid.UUID,
        bookmark_repository: AsyncMongoDBBookmarkRepository = fastapi.Depends(get_bookmark_repository),
) -> List[http_bookmarks_models.Bookmark]:
    bookmarks = await bookmark_repository.get_user_bookmarks(user_id)
    return [http_bookmarks_models.Bookmark(**bookmark.to_dict(False)) for bookmark in bookmarks]
