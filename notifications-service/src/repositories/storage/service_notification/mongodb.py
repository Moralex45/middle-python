from __future__ import annotations

import uuid

from motor import motor_asyncio

import src.core.config as project_config
from src.models.storage import service_notification as storage_notifications
from src.repositories.storage.service_notification.base import \
    AsyncNotificationsRepositoryProtocol


class AsyncMongoDBNotificationRepository(AsyncNotificationsRepositoryProtocol):
    def __init__(
            self,
            mongodb_instance: motor_asyncio.AsyncIOMotorClient,
    ):
        database = mongodb_instance[
            project_config.get_settings().mongodb_settings.mongodb_database
        ]
        self.collection: motor_asyncio.AsyncIOMotorCollection = database[
            project_config.get_settings().mongodb_settings.events_notifications_collection
        ]

    async def create_notification(
            self,
            type: str,  # noqa : VNE003
            content: dict,
            sending_time_timestamp: int | None = None,
            sending_timeout: int | None = None,
    ) -> storage_notifications.ServiceNotification:
        notification = storage_notifications.ServiceNotification(
            _id=uuid.uuid4(),
            type=type,
            content=content,
        )

        if sending_time_timestamp is not None:
            notification.sending_time_timestamp = sending_time_timestamp

        if sending_timeout is not None:
            notification.sending_timeout = sending_timeout

        await self.collection.insert_one(notification.to_dict())

        return notification
