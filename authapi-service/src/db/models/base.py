import datetime
import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, TIMESTAMP
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), nullable=False, unique=True, primary_key=True, default=uuid.uuid4)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now(), onupdate=datetime.datetime.now())  # noqa

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)
