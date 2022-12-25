import uuid

from src.models.base import Base
from src.models.addition.addition import ProductType


class UserPurchase(Base):
    user_id: uuid.UUID
    product_type: ProductType
    product_id: uuid.UUID
    payment_id: uuid.UUID


class UserPurchaseIN(Base):
    user_id: uuid.UUID
    product_type: ProductType
    product_id: uuid.UUID
    payment_id: uuid.UUID | None
    subscription_id: uuid.UUID
