from http import HTTPStatus
from uuid import UUID

from api.v1.tools import PaginatedParams
from core.constants.exception_details import PERSON_NOT_FOUND
from fastapi import APIRouter, Depends, HTTPException

from core.utils import verify_token
from models.film import FilmBase
from models.person import Person
from services.person import PersonService, get_persons_service

router = APIRouter()


@router.get('/search',
            response_model=list[Person],
            description='Полнотекстовый поиск по участникам кинопроизведения',
            summary='Endpoint позволяет проводить поиск по участникам кинопроизведений',
            response_description='Лист объектов Person',
            tags=['Полнотекстовый поиск'])
async def film_search(query: str,
                      paginated_parameters: PaginatedParams = Depends(PaginatedParams.query_paginated_parameters),
                      person_service: PersonService = Depends(get_persons_service)) -> list[Person]:
    page_number, page_size = paginated_parameters.page_number, paginated_parameters.page_size
    persons = await person_service.search(page_number, page_size, query)

    return persons


@router.get('/{person_id}',
            response_model=Person,
            description='Детальная информация участника кинопроизведения',
            summary='Endpoint позволяет получить детальную информацию по участнику кинопроизведения',
            response_description='Объект Person',
            tags=['Доступ к элементу по id'])
async def person_details(person_id: UUID,
                         person_service: PersonService = Depends(get_persons_service)) -> Person:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PERSON_NOT_FOUND)

    return Person(**person.dict())


@router.get('/{person_id}/film',
            response_model=list[FilmBase],
            description='Вывод фильмов по участнику кинопроизведения',
            summary='Endpoint позволяет получить информацию по всем кинопроизведениям конкретного человека',
            response_description='Лист объектов FilmBase',
            tags=['Доступ ко всем элементам'])
async def person_films(person_id: UUID,
                       person_service: PersonService = Depends(get_persons_service)) -> list[FilmBase]:
    films = await person_service.get_person_films(person_id)
    if films is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PERSON_NOT_FOUND)
    return films
