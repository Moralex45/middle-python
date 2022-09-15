from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from base import Base

from core.config import get_settings_instance

engine = create_engine(
    get_settings_instance().postgres_connection_url,
    echo=True
)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


Base.query = db_session.query_property()
