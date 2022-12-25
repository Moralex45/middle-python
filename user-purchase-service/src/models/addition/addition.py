import enum


class ProductType(enum.Enum):
    FILM = 'film'
    SUBSCRIPTION = 'subscription'


class PaymentStatus(enum.Enum):
    succeed = 'succeeded'
    canseled = 'canseled'
    refunded = 'refunded'
