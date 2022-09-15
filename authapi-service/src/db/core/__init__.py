from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from db.models.base import Base

from core.config import get_settings_instance

engine = create_engine(
    get_settings_instance().POSTGRES_DSN,
    echo=True,
    connect_args={'options': f'-csearch_path={get_settings_instance().POSTGRES_SCHEMA}'}
)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base.query = db_session.query_property()
