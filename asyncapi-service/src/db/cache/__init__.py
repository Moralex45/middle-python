from db.cache.base import AsyncCacheService


async def get_cache_service() -> AsyncCacheService:
    return cache_service


cache_service: AsyncCacheService | None = None
