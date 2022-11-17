from __future__ import annotations

import fastapi

import src.models.http.service_notification as http_service_notifications
from src.repositories.storage.service_notification import (
    AsyncMongoDBNotificationRepository, get_service_notification_repository)

router = fastapi.APIRouter(prefix='/api/v1/service_notification')


@router.post(
    '/',
    response_model=http_service_notifications.ServiceNotification,
    status_code=fastapi.status.HTTP_201_CREATED,
    description='Создание нотификации от внутренних сервисов',
    summary='Endpoint позволяет создать нотификацию от внутренних сервисов',
    tags=['Закладки'],
)
async def create_notification(
        http_notification: http_service_notifications.ServiceNotificationCreation,
        service_notification_repository: AsyncMongoDBNotificationRepository = fastapi.Depends(
            get_service_notification_repository,
        ),
) -> http_service_notifications.ServiceNotification:
    repository_notification = await service_notification_repository.create_notification(
        http_notification.type,
        http_notification.content,
        http_notification.sending_time_timestamp,
        http_notification.sending_timeout,
    )
    # TODO implement sending to rabbitmq
    return http_service_notifications.ServiceNotification(**repository_notification.to_dict(False))
