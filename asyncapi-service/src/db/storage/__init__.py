from db.storage.base import AsyncStorageService


async def get_storage_service() -> AsyncStorageService:
    return storage_service


storage_service: AsyncStorageService | None = None
