import time

import pytest

from db.core import db_session
from db.models.permissions import Permission, RolePermissions
from db.models.roles import Role
from functional.testdata.database_fake_data import roles, permissions, roles_permissions


@pytest.fixture(scope='session')
def clean_database():
    from src.db.models.users import User, UserData, AuthHistory  # noqa
    from src.db.models.roles import Role, UserRole  # noqa
    from src.db.models.permissions import Permission, RolePermissions  # noqa
    from src.db.core import Base, engine
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture(scope='session')
def database_session():
    return db_session


@pytest.fixture(scope='session')
def generate_roles(database_session):
    with database_session():
        db_roles = [Role(**role) for role in roles]
        for db_role in db_roles:
            database_session.add(db_role)

        database_session.commit()


@pytest.fixture(scope='session')
def generate_permissions(database_session):
    with database_session():
        db_permissions = [Permission(**permission) for permission in permissions]
        for db_permission in db_permissions:
            database_session.add(db_permission)

        database_session.commit()


@pytest.fixture(scope='session')
def generate_roles_permissions(database_session, generate_roles, generate_permissions):
    with database_session():
        db_roles_permissions = [RolePermissions(**role_permission) for role_permission in roles_permissions]
        for db_roles_permission in db_roles_permissions:
            database_session.add(db_roles_permission)

        database_session.commit()

