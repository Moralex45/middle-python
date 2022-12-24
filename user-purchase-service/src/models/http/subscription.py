from src.models.base import Base


class Subscription(Base):
    description: str
    price: int
    duration: int


class SubscriptionPUT(Base):
    description: str | None
    price: int | None
    duration: int | None
