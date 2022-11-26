from __future__ import annotations

import functools

import fastapi

from src.repositories.amqp_producer.admin_notification.rabbitmq import \
    AsyncRabbitMQNotificationRepository
from src.services.amqp_producer import get_rabbitmq_connection_instance


@functools.lru_cache()
def get_amqp_producer_service_notification_repository(
        rabbitmq_connection=fastapi.Depends(get_rabbitmq_connection_instance),
) -> AsyncRabbitMQNotificationRepository:
    return AsyncRabbitMQNotificationRepository(rabbitmq_producer_instance=rabbitmq_connection)
