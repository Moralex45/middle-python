import enum


class ProductType(enum.Enum):
    FILM = 'film'
    SUBSCRIPTION = 'subscription'


class PaymentStatus(enum.Enum):
    succeed = 'succeed'
    canseled = 'canseled'
    refunded = 'refunded'
