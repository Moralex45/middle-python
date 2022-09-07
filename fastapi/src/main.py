import aioredis
import uvicorn
from aioredis import Redis
from elasticsearch import AsyncElasticsearch

from api.v1 import films, genres, persons
from core.config import get_settings_instance
from db import cache, storage
from db.cache.redis import AsyncRedisCacheService
from db.storage.elastic import AsyncElasticStorageService
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title=get_settings_instance().PROJECT_NAME,
    description='Сервиса получения информации из ES  жанрам, персоналиям и фильмам',
    version='0.1',
    redoc_url='/api/docs/redoc',
    docs_url='/api/docs/openapi',
    openapi_url='/api/docs/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    redis_pool: Redis = await aioredis.create_redis_pool(
        (get_settings_instance().REDIS_HOST, get_settings_instance().REDIS_PORT),
        minsize=10,
        maxsize=20)
    cache.cache_service = AsyncRedisCacheService(redis_pool)

    es = AsyncElasticsearch(hosts=[get_settings_instance().elastic_connection_url])
    storage.storage_service = AsyncElasticStorageService(es)


@app.on_event('shutdown')
async def shutdown():
    await cache.cache_service.close()
    await storage.storage_service.close()


app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['genres'])
app.include_router(persons.router, prefix='/api/v1/persons', tags=['persons'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True
    )
