from http import HTTPStatus
from uuid import UUID

from api.v1.tools import PaginatedParams
from core.constants.exception_details import FILM_NOT_FOUND
from fastapi import APIRouter, Depends, HTTPException, Query
from models.film import Film, FilmBase
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get('/search',
            response_model=list[FilmBase],
            description='Полнотекстовый поиск по кинопроизведениям',
            summary='Endpoint позволяет проводить поиск по кинопроизведениям',
            response_description='Лист объектов FilmBase',
            tags=['Полнотекстовый поиск элементов'])
async def film_search(
        _query: str = Query(alias='query'),
        paginated_parameters: PaginatedParams = Depends(PaginatedParams.query_paginated_parameters),
        film_service: FilmService = Depends(get_film_service)) -> list[FilmBase]:
    page_number, page_size = paginated_parameters.page_number, paginated_parameters.page_size
    films = await film_service.search(page_number, page_size, _query)

    return films


@router.get('/{film_id}',
            response_model=Film,
            description='Детальная информация по кинопроизведению',
            summary='Endpoint позволяет получить фильм по его uuid',
            response_description='Объект Film',
            tags=['Доступ к элементу по id'])
async def film_details(film_id: UUID,
                       film_service: FilmService = Depends(get_film_service)) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FILM_NOT_FOUND)

    return film


@router.get('/',
            response_model=list[FilmBase],
            description='Список всех кинопроизведений',
            summary='Endpoint позволяет получить список кинопроизведений',
            response_description='Лист объектов FilmBase',
            tags=['Доступ ко всем элементам'])
async def film_list(_filter: UUID | None = Query(alias='filter[genre]', default=None),
                    _sort: str = Query(alias='sort'),
                    paginated_parameters: PaginatedParams = Depends(PaginatedParams.query_paginated_parameters),
                    film_service: FilmService = Depends(get_film_service)):
    page_number, page_size = paginated_parameters.page_number, paginated_parameters.page_size
    films = await film_service.get_list_filter_sort_paginate(page_size,
                                                             page_number,
                                                             _sort.replace('-', ''),
                                                             True if '-' in _sort else False,
                                                             _filter)
    if not films:
        return []
    return films
