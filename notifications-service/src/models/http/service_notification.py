import uuid

import pydantic

from src.core.constants.service_notification import ServiceNotificationType
from src.models.base import Base


class ServiceNotificationCreation(Base):
    type: ServiceNotificationType  # noqa: VNE003
    content: dict
    sending_time_timestamp: str | None
    sending_timeout: int | None

    @pydantic.validator('sending_timeout')
    def prevent_negative_timeout(cls, value: int):
        if value < 0:
            raise ValueError('Timeout timestamp can not be negative')
        return value

    @pydantic.root_validator()
    def check_sending_time_or_timeout(cls, values: dict):
        if (values.get('sending_timeout') is not None) and (values.get('sending_time_timestamp') is not None):
            raise ValueError('Only "sending_time_timestamp" or "sending_timeout" required')
        return values


class ServiceNotification(ServiceNotificationCreation):
    id: uuid.UUID  # noqa: VNE003
