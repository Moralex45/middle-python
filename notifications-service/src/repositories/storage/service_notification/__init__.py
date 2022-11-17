from __future__ import annotations

import functools

import fastapi

from src.repositories.storage.service_notification.mongodb import AsyncMongoDBNotificationRepository
from src.services.storage import get_mongodb_instance


@functools.lru_cache()
def get_service_notification_repository(
        mongodb_instance=fastapi.Depends(get_mongodb_instance),
) -> AsyncMongoDBNotificationRepository:
    return AsyncMongoDBNotificationRepository(mongodb_instance)
