from __future__ import annotations

import aio_pika

import src.core.config as project_config
from src.models.amqp_producer import admin_notification as amqp_notifications
from src.repositories.amqp_producer.admin_notification.base import \
    AsyncNotificationsAMQPRepositoryProtocol


class AsyncRabbitMQNotificationRepository(AsyncNotificationsAMQPRepositoryProtocol):
    def __init__(
            self,
            rabbitmq_producer_instance: aio_pika.RobustConnection,
    ):
        self.rabbitmq_producer = rabbitmq_producer_instance

    async def publish_notification(self, amqp_service_notification: amqp_notifications.AdminServiceNotification) -> None:
        async with self.rabbitmq_producer:
            routing_key = project_config.RabbitMQSettings.routing_key
            channel = await self.rabbitmq_producer.channel()

            await channel.default_exchange.publish(
                aio_pika.Message(body=amqp_service_notification.json().encode()),
                routing_key=routing_key,
            )
