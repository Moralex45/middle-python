from enum import Enum


class ServiceNotificationType(Enum):
    REGISTRATION = 'registration'
    LIKE = 'like'
    NEW_SERIES = 'new_series'
    MAILING = 'mailing'

    @classmethod
    def has_value(cls, value: str) -> bool:
        return value in cls._value2member_map_
