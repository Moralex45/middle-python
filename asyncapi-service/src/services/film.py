from functools import lru_cache
from uuid import UUID

from fastapi import Depends

from core.config import get_settings_instance
from db.cache import get_cache_service
from db.cache.base import AsyncCacheService
from db.storage import get_storage_service
from db.storage.elastic import AsyncElasticStorageService
from models.film import Film, FilmBase


class FilmService:
    def __init__(self, cache_service: AsyncCacheService, storage_service: AsyncElasticStorageService):
        self.cache_service: AsyncCacheService = cache_service
        self.storage_service: AsyncElasticStorageService = storage_service

    async def get_by_id(self, film_id: UUID) -> Film | None:
        redis_key: str = f'movies::uuid::{str(film_id)}'
        film = await self.cache_service.get_single(redis_key, Film)

        if not film:
            film = await self.storage_service.get_by_id(id=str(film_id), index='movies', base_class=Film)
            if not film:
                return None
            await self.cache_service.set_single(redis_key, film, get_settings_instance().FILM_CACHE_EXPIRE_IN_SECONDS)
        return film

    async def get_list_filter_sort_paginate(self,
                                            page_size: int,
                                            page_number: int,
                                            sort_field: str,
                                            sort_desc: bool = True,
                                            filter_genre_id: UUID | None = None) -> None | list[FilmBase]:
        redis_key = f'movies::' \
            f'page_size::{page_size}::' \
            f'page_number::{page_number}::' \
            f'sort_field::{sort_field}::' \
            f'sort_desc::{sort_desc}::' \
            f'filter_genre_id::{filter_genre_id}'
        films = await self.cache_service.get_list(redis_key, FilmBase)
        if not films:
            body = {
                'from': (page_number - 1) * page_size,
                'size': page_size,
                'sort': [{sort_field: {'order': 'desc' if sort_desc else 'asc'}}]
            }
            if filter_genre_id is not None:
                body['query'] = {
                    'nested': {
                        'path': 'genre',
                        'query': {
                            'bool': {
                                'filter': {
                                    'term': {
                                        'genre.id': filter_genre_id
                                    }
                                }
                            }
                        }
                    }
                }
            films = await self.storage_service.search(index='movies', body=body, base_class=FilmBase)
            if not films:
                return []
            await self.cache_service.set_list(redis_key, films, get_settings_instance().FILM_CACHE_EXPIRE_IN_SECONDS)
        return films

    async def search(self, page_number: int, page_size: int, query: str) -> list[FilmBase] | None:
        redis_key = f'movies::page_size::{page_size}::page_number::{page_number}::query::{query}'
        films = await self.cache_service.get_list(redis_key, FilmBase)
        if not films:
            body = {
                'from': (page_number - 1) * page_size,
                'size': page_size,
                'query': {
                    'bool': {
                        'should': [
                            {
                                'nested': {
                                    'path': 'genre',
                                    'query': {
                                        'multi_match': {
                                            'query': query,
                                            'fuzziness': 'auto',
                                            'fields': ['genre.name']
                                        }
                                    }
                                }
                            },
                            {
                                'multi_match': {
                                    'query': query,
                                    'fuzziness': 'auto',
                                    'fields': [
                                        'actors_names',
                                        'writers_names',
                                        'directors_names',
                                        'title',
                                        'description',
                                    ]
                                }
                            }
                        ]
                    }
                }
            }
            films = await self.storage_service.search(index='movies', body=body, base_class=FilmBase)
            if not films:
                return []
            await self.cache_service.set_list(redis_key, films, get_settings_instance().FILM_CACHE_EXPIRE_IN_SECONDS)
        return films


@lru_cache()
def get_film_service(cache_service: AsyncCacheService = Depends(get_cache_service),
                     storage_service: AsyncElasticStorageService = Depends(get_storage_service)) -> FilmService:
    return FilmService(cache_service, storage_service)
