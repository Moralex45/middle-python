from functools import lru_cache
from uuid import UUID

from fastapi import Depends

from core.config import get_settings_instance
from db.cache import AsyncCacheService, get_cache_service
from db.storage import get_storage_service
from db.storage.elastic import AsyncElasticStorageService
from models.genre import Genre


class GenreService:
    def __init__(self, cache_service: AsyncCacheService, storage_service: AsyncElasticStorageService):
        self.cache_service = cache_service
        self.storage_service = storage_service

    async def get_by_id(self, genre_id: UUID) -> Genre | None:
        redis_key: str = f'genres::uuid::{str(genre_id)}'
        genre = await self.cache_service.get_single(redis_key, Genre)
        if not genre:
            genre = await self.storage_service.get_by_id(id=str(genre_id), index='genres', base_class=Genre)
            if not genre:
                return None
            await self.cache_service.set_single(redis_key,
                                                genre,
                                                expire=get_settings_instance().GENRE_CACHE_EXPIRE_IN_SECONDS)
        return genre

    async def get_list(self) -> list[Genre]:
        redis_key: str = 'genres::all'
        genres = await self.cache_service.get_list(redis_key, Genre)
        if not genres:
            genres = await self.storage_service.search(index='genres', body={}, base_class=Genre)
            if not genres:
                return []
            await self.cache_service.set_list(redis_key, genres, get_settings_instance().GENRE_CACHE_EXPIRE_IN_SECONDS)
        return genres


@lru_cache()
def get_genre_service(cache_service: AsyncCacheService = Depends(get_cache_service),
                      storage_service: AsyncElasticStorageService = Depends(get_storage_service)) -> GenreService:
    return GenreService(cache_service, storage_service)
