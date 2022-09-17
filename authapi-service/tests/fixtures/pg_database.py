import time

import pytest


@pytest.fixture(scope='session')
def clean_database():
    from src.db.models.users import User, UserData, AuthHistory  # noqa
    from src.db.models.roles import Role, UserRole  # noqa
    from src.db.models.permissions import Permission, RolePermissions  # noqa
    from src.db.core import Base, engine
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
