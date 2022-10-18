import datetime
import uuid

from sqlalchemy import TIMESTAMP, Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4) # noqa
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now)
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def __repr__(self):
        return '<{0.__class__.__name__}(id={0.id!r})>'.format(self)
