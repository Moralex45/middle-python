from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src.core.config import get_settings_instance
from src.db.models.base import Base

engine = create_engine(
    get_settings_instance().POSTGRES_DSN,
    echo=False,
    connect_args={'options': f'-csearch_path={get_settings_instance().POSTGRES_SCHEMA}'},
)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base.query = db_session.query_property()
