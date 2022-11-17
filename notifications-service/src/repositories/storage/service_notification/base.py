from __future__ import annotations

from abc import ABC, abstractmethod

import src.models.storage.service_notification as storage_notifications


class AsyncNotificationsRepositoryProtocol(ABC):
    @abstractmethod
    async def create_notification(
            self,
            type: str,  # noqa : VNE003
            content: dict,
            sending_time_timestamp: int | None = None,
            sending_timeout: int | None = None,
    ) -> storage_notifications.ServiceNotification:
        raise NotImplementedError
