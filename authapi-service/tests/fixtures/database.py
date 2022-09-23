import pytest

from src.db.core import db_session
from src.db.models.permissions import Permission, RolePermissions
from src.db.models.roles import Role, UserRole
from src.db.models.users import User
from tests.functional.testdata.database_fake_data import roles, permissions, roles_permissions, users_roles, users, \
    super_users


@pytest.fixture()
def clean_database():
    from src.db.models.users import User, UserData, AuthHistory  # noqa
    from src.db.models.roles import Role, UserRole  # noqa
    from src.db.models.permissions import Permission, RolePermissions  # noqa
    from src.db.core import Base, engine
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture()
def database_session():
    return db_session


@pytest.fixture()
def generate_roles(database_session):
    with database_session():
        db_roles = [Role(**role) for role in roles]
        for db_role in db_roles:
            database_session.add(db_role)

        database_session.commit()


@pytest.fixture()
def generate_permissions(database_session):
    with database_session():
        db_permissions = [Permission(**permission) for permission in permissions]
        for db_permission in db_permissions:
            database_session.add(db_permission)

        database_session.commit()


@pytest.fixture()
def generate_roles_permissions(database_session, generate_roles, generate_permissions):
    with database_session():
        for role_permission in roles_permissions:
            db_role_permission = RolePermissions(id=role_permission['id'],
                                                 role_id=role_permission['role_id'],
                                                 perm_id=role_permission['permission_id'])
            database_session.add(db_role_permission)

        database_session.commit()


@pytest.fixture()
def generate_users(database_session):
    with database_session():
        db_users = [User(**user) for user in users]
        for db_user in db_users:
            database_session.add(db_user)

        database_session.commit()


@pytest.fixture()
def generate_super_users(database_session):
    with database_session():
        db_users = [User(**user) for user in super_users]
        for db_user in db_users:
            database_session.add(db_user)

        database_session.commit()


@pytest.fixture()
def generate_users_roles(database_session, generate_roles_permissions, generate_users):
    with database_session():
        for user_role in users_roles:
            db_user_role = UserRole(id=user_role['id'],
                                    user_id=user_role['user_id'],
                                    role_id=user_role['role_id'])
            database_session.add(db_user_role)

        database_session.commit()
