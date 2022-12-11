from __future__ import annotations

from abc import ABC, abstractmethod

import src.models.storage.admin_notification as admin_notifications


class AsyncNotificationsStorageRepositoryProtocol(ABC):
    @abstractmethod
    async def create_notification(
            self,
            type: str,  # noqa : VNE003
            content: str,
            recepients: list,
            sending_time_timestamp: int | None = None,
            sending_timeout: int | None = None,
    ) -> admin_notifications.ServiceNotification:
        raise NotImplementedError
