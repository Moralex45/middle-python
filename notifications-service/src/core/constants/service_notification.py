from enum import Enum


class ServiceNotificationType(Enum):
    REGISTRATION = 'registration'
    LIKE = 'like'
    NEW_SERIES = 'new_series'
    MAILING = 'mailing'
