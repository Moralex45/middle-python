from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from core.constants.exception_details import GENRE_NOT_FOUND
from core.utils import verify_auth_tokens
from models.genre import Genre
from services.genre import GenreService, get_genre_service

router = APIRouter()


@router.get('/',
            response_model=list[Genre | None],
            description='Список всех жанров',
            summary='Endpoint позволяет получить список жанров',
            response_description='Лист объектов Genre',
            tags=['Доступ ко всем элементам'],
            dependencies=[Depends(verify_auth_tokens)])
async def all_genres(genre_service: GenreService = Depends(get_genre_service)) -> list[Genre]:
    genres = await genre_service.get_list()
    if not genres:
        return []

    return genres


@router.get('/{genre_id}',
            response_model=Genre,
            description='Детальная информация по жанру',
            summary='Endpoint позволяет получить детальную информацию по жанру',
            response_description='Объект Genre',
            tags=['Доступ ко всем элементам'],
            dependencies=[Depends(verify_auth_tokens)])
async def genre_details(genre_id: UUID, genre_service: GenreService = Depends(get_genre_service)) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=GENRE_NOT_FOUND)

    return genre
