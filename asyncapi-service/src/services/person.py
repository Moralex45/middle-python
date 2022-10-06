from functools import lru_cache
from uuid import UUID

import backoff
from elasticsearch import NotFoundError, exceptions
from fastapi import Depends

from core.config import get_settings_instance
from db.cache import AsyncCacheService, get_cache_service
from db.storage import get_storage_service
from db.storage.elastic import AsyncElasticStorageService
from models.film import FilmBase
from models.person import Person
from services.es_queries import person_roles_find


class PersonService:
    def __init__(self, cache_service: AsyncCacheService, storage_service: AsyncElasticStorageService):
        self.cache_service = cache_service
        self.storage_service = storage_service

    async def get_by_id(self, person_id: UUID) -> None | Person:
        redis_key: str = f'persons::uuid::{str(person_id)}'
        person = await self.cache_service.get_single(redis_key, Person)
        if not person:
            person = await self._get_person_from_elastic(person_id)
            if not person:
                return None
            await self.cache_service.set_single(redis_key,
                                                person,
                                                get_settings_instance().PERSON_CACHE_EXPIRE_IN_SECONDS)
        return person

    async def search(self, page_number: int, page_size: int, query: str) -> list[Person] | None:
        redis_key = f'persons::page_size::{page_size}::page_number::{page_number}::query::{query}'
        persons = await self.cache_service.get_list(redis_key, Person)
        if not persons:
            persons = await self._get_person_search_from_elastic(page_number, page_size, query)
            if not persons:
                return []
            await self.cache_service.set_list(redis_key,
                                              persons,
                                              get_settings_instance().PERSON_CACHE_EXPIRE_IN_SECONDS)
        return persons

    async def get_person_films(self, person_id: UUID) -> list[FilmBase] | None:
        redis_key = f'movies::person_films::{str(person_id)}'
        films = await self.cache_service.get_list(redis_key, FilmBase)
        if not films:
            person = await self.get_by_id(person_id)
            if not person:
                return None
            films = await self._get_person_films_from_elastic(person.full_name)
            if not films:
                return []
            await self.cache_service.set_list(redis_key, films, get_settings_instance().FILM_CACHE_EXPIRE_IN_SECONDS)
        return films

    @backoff.on_exception(backoff.expo, [exceptions.ConnectionError], max_time=10)
    async def _get_person_search_from_elastic(self,
                                              page_number: int,
                                              page_size: int,
                                              query: str) -> list[Person] | None:
        person = list()
        body = {
            'from': (page_number - 1) * page_size,
            'size': page_size,
            'query': {
                'multi_match': {
                    'query': query,
                    'fuzziness': 'auto',
                    'fields': [
                        'full_name'
                    ]
                }
            }
        }

        try:
            doc = await self.storage_service.elastic.search(
                index='persons',
                body=body,
            )
        except NotFoundError:
            return None

        for element in doc['hits']['hits']:
            person.append(await self.get_by_id(element['_source']['id']))

        return person

    @backoff.on_exception(backoff.expo, [exceptions.ConnectionError], max_time=10)
    async def _get_person_from_elastic(self, person_id: UUID) -> Person | None:
        try:
            doc = await self.storage_service.elastic.get('persons', person_id)
        except NotFoundError:
            return None

        person_name = doc['_source']['full_name']
        person_roles, film_ids = await self._get_person_roles_filmids_from_elastic(person_name)
        return Person.from_es(**doc['_source'], role=person_roles, film_ids=film_ids)

    @backoff.on_exception(backoff.expo, [exceptions.ConnectionError], max_time=10)
    async def _get_person_roles_filmids_from_elastic(self, person_name: str):
        roles = list()
        film_ids = list()
        for role, query in person_roles_find.items():
            results = await self.storage_service.elastic.search(index='movies', body=query % person_name)
            for entry in results['hits']['hits']:
                if len(entry['_source']) > 0:
                    roles.append(role)
                    film_ids.append(entry['_source']['id'])
        return list(set(roles)), film_ids

    @backoff.on_exception(backoff.expo, [exceptions.ConnectionError], max_time=10)
    async def _get_person_films_from_elastic(self, person_name: str) -> list[FilmBase]:
        films = list()
        for query in person_roles_find.values():
            body = query % person_name
            results = await self.storage_service.search(index='movies', body=body, base_class=FilmBase)
            films.extend(results if results is not None else [])
        return films


@lru_cache()
def get_persons_service(cache_service: AsyncCacheService = Depends(get_cache_service),
                        storage_service: AsyncElasticStorageService = Depends(get_storage_service)) -> PersonService:
    return PersonService(cache_service, storage_service)
