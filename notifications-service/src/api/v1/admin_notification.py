from __future__ import annotations

import fastapi

import src.models.http.admin_notification as http_admin_notifications
import src.models.amqp_producer.admin_notification as amqp_admin_notifications
from src.repositories.storage.admin_notification import (
    AsyncMongoDBNotificationStorageRepository, get_storage_service_notification_repository)
from src.repositories.amqp_producer.service_notification import (
    AsyncRabbitMQNotificationRepository, get_amqp_producer_service_notification_repository)

router = fastapi.APIRouter(prefix='/api/v1/admin_notification')


@router.post(
    '/',
    response_model=http_admin_notifications.AdminServiceNotification,
    status_code=fastapi.status.HTTP_201_CREATED,
    description='Админка для нотификаций',
    summary='Endpoint для управления нотификациями через админку',
)
async def create_notification(
    http_notification: http_admin_notifications.AdminNotificationCreation,
    storage_service_notification_repository: AsyncMongoDBNotificationStorageRepository = fastapi.Depends(
        get_storage_service_notification_repository,
    ),
    amqp_producer_service_notification_repository: AsyncRabbitMQNotificationRepository = fastapi.Depends(
        get_amqp_producer_service_notification_repository,
    ),
) -> http_admin_notifications.AdminServiceNotification:
    repository_notification = await storage_service_notification_repository.create_notification(
        http_notification.type,
        http_notification.content,
        http_notification.recepients,
        http_notification.sending_time_timestamp,
        http_notification.sending_timeout,
    )

    await amqp_producer_service_notification_repository.publish_notification(
        amqp_admin_notifications.ServiceNotification(**repository_notification.to_dict()),
    )
    return http_admin_notifications.AdminServiceNotification(**repository_notification.to_dict(False))
