from __future__ import annotations

from abc import ABC, abstractmethod

import src.models.amqp_producer.admin_notification as amqp_notifications


class AsyncNotificationsAMQPRepositoryProtocol(ABC):
    @abstractmethod
    async def publish_notification(
            self,
            amqp_service_notification: amqp_notifications.ServiceNotification,
    ) -> None:
        raise NotImplementedError
