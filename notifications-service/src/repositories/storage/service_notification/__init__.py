from __future__ import annotations

import functools

import fastapi

from src.repositories.storage.service_notification.mongodb import \
    AsyncMongoDBNotificationStorageRepository
from src.services.storage import get_mongodb_instance


@functools.lru_cache()
def get_storage_service_notification_repository(
        mongodb_instance=fastapi.Depends(get_mongodb_instance),
) -> AsyncMongoDBNotificationStorageRepository:
    return AsyncMongoDBNotificationStorageRepository(mongodb_instance)
