from __future__ import annotations

import uuid

from motor import motor_asyncio

import src.core.config as project_config
from src.models.storage import admin_notification as admin_notifications
from src.repositories.storage.admin_notification.base import \
    AsyncNotificationsStorageRepositoryProtocol


class AsyncMongoDBNotificationStorageRepository(AsyncNotificationsStorageRepositoryProtocol):
    def __init__(
            self,
            mongodb_instance: motor_asyncio.AsyncIOMotorClient,
    ):
        database = mongodb_instance[
            project_config.get_settings().mongodb_settings.mongodb_database
        ]
        self.collection: motor_asyncio.AsyncIOMotorCollection = database[
            project_config.get_settings().mongodb_settings.admin_notifications_collection
        ]

    async def create_notification(
            self,
            type: str,  # noqa : VNE003
            content: str,
            recepients: list,
            sending_time_timestamp: int | None = None,
            sending_timeout: int | None = None,
    ) -> admin_notifications.ServiceNotification:
        notification = admin_notifications.ServiceNotification(
            _id=uuid.uuid4(),
            type=type,
            content=content,
            recepients=recepients,
        )

        if sending_time_timestamp is not None:
            notification.sending_time_timestamp = sending_time_timestamp

        if sending_timeout is not None:
            notification.sending_timeout = sending_timeout

        await self.collection.insert_one(notification.to_dict())

        return notification
