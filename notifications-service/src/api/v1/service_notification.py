from __future__ import annotations

import datetime

import fastapi

import src.models.http.service_notification as http_service_notifications
import src.models.amqp_producer.service_notification as amqp_service_notifications
from src.repositories.storage.service_notification import (
    AsyncMongoDBNotificationStorageRepository, get_storage_service_notification_repository)
from src.repositories.amqp_producer.service_notification import (
    AsyncRabbitMQNotificationRepository, get_amqp_producer_service_notification_repository)
from src.utils.schedule import scheduler, get_job_id


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
        storage_service_notification_repository: AsyncMongoDBNotificationStorageRepository = fastapi.Depends(
            get_storage_service_notification_repository,
        ),
        amqp_producer_service_notification_repository: AsyncRabbitMQNotificationRepository = fastapi.Depends(
            get_amqp_producer_service_notification_repository,
        ),
) -> http_service_notifications.ServiceNotification:
    repository_notification = await storage_service_notification_repository.create_notification(
        http_notification.type,
        http_notification.content,
        http_notification.sending_time_timestamp,
        http_notification.sending_timeout,
    )

    possible_sending_time: datetime.datetime | None = None

    if repository_notification.sending_timeout is not None:
        possible_sending_time = datetime.datetime.now() + datetime.timedelta(
            seconds=repository_notification.sending_timeout,
        )

    elif repository_notification.sending_time_timestamp is not None:
        possible_sending_time = datetime.datetime.fromtimestamp(repository_notification.sending_time_timestamp)

    if possible_sending_time is not None:
        scheduler.add_job(func=amqp_producer_service_notification_repository.publish_notification,
                          kwargs=repository_notification.to_dict(),
                          id=get_job_id(repository_notification),
                          trigger='date',
                          run_date=possible_sending_time,
                          replace_existing=True)
    else:
        await amqp_producer_service_notification_repository.publish_notification(
            amqp_service_notifications.ServiceNotification(**repository_notification.to_dict()),
        )
    return http_service_notifications.ServiceNotification(**repository_notification.to_dict(False))
