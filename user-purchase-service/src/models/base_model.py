import uuid

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

from src.db.sqlalchemy.core import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4)  # noqa
