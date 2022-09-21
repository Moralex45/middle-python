import click
from flask import Flask

__all__ = ('create_app', 'create_raw_app')


def create_raw_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    configure_blueprints(app)

    return app


def create_app() -> Flask:
    app = create_raw_app()
    configure_db()
    configure_cli(app)

    return app


def configure_db() -> None:
    from src.db.core import Base, engine
    from src.db.models.permissions import Permission, RolePermissions  # noqa
    from src.db.models.roles import Role, UserRole  # noqa
    from src.db.models.users import AuthHistory, User, UserData  # noqa
    Base.metadata.create_all(bind=engine)


def configure_jwt():
    pass


def configure_blueprints(app) -> None:
    from src.api.v1.auth import blueprint as auth_blueprint
    from src.api.v1.crud.role_permission import \
        blueprint as role_permission_blueprint
    from src.api.v1.crud.user_role import blueprint as user_role_blueprint
    from src.api.v1.crud.role import blueprint as role_blueprint
    from src.api.v1.crud.permission import blueprint as permission_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(role_blueprint)
    app.register_blueprint(permission_blueprint)
    app.register_blueprint(role_permission_blueprint)
    app.register_blueprint(user_role_blueprint)


def configure_cli(app):
    @app.cli.command('createdatabase')
    def create_database():
        configure_db()

    @app.cli.command('createdefault')
    def create_default_data():
        from src.db.core import db_session
        from src.db.models.roles import Role
        from src.db.models.permissions import RolePermissions
        from src.db.models.permissions import Permission
        from src.core.constants import (
            ADMIN_ROLE,
            SAMPLE_USER_ROLE,
            CAN_ADD_PERMISSION,
            CAN_ADD_ROLE,
            CAN_ADD_ROLE_PERMISSION,
            CAN_ADD_USER_ROLE,
            CAN_EDIT_PROFILE
        )

        with db_session() as session:
            db_role_admin = Role(
                **ADMIN_ROLE
            )

            db_role_user = Role(
                **SAMPLE_USER_ROLE
            )

            db_can_add_role = Permission(
                **CAN_ADD_ROLE
            )

            db_can_add_permission = Permission(
                **CAN_ADD_PERMISSION
            )

            db_can_add_role_permission = Permission(
                **CAN_ADD_ROLE_PERMISSION
            )

            db_can_add_user_role = Permission(
                **CAN_ADD_USER_ROLE
            )
            
            db_can_edit_profile = Permission(
                **CAN_EDIT_PROFILE
            )

            session.add_all(
                [
                    db_role_admin,
                    db_role_user,
                    db_can_add_role,
                    db_can_add_permission,
                    db_can_add_role_permission,
                    db_can_add_user_role,
                    db_can_edit_profile
                ]
            )
            session.commit()

            role_admin_can_add_role = RolePermissions(
                role_id=db_role_admin.id,
                perm_id=db_can_add_role.id
            )
            role_admin_can_add_permission = RolePermissions(
                role_id=db_role_admin.id,
                perm_id=db_can_add_permission.id
            )
            role_admin_can_add_role_permission = RolePermissions(
                role_id=db_role_admin.id,
                perm_id=db_can_add_role_permission.id
            )
            role_admin_can_add_user_role = RolePermissions(
                role_id=db_role_admin.id,
                perm_id=db_can_add_user_role.id
            )
            role_sample_user_can_edit_profile = RolePermissions(
                role_id=db_role_user.id,
                perm_id=db_can_edit_profile.id
            )

            session.add_all(
                [
                    role_admin_can_add_role,
                    role_admin_can_add_permission,
                    role_admin_can_add_role_permission,
                    role_admin_can_add_user_role,
                    role_sample_user_can_edit_profile
                ]
            )
            session.commit()

    @app.cli.command('createsuperuser')
    @click.argument('username')
    @click.argument('password')
    def create_superuser(username, password):
        from src.db.models.users import User
        from src.db.models.roles import Role, UserRole
        from src.core.constants import ADMIN_ROLE
        from src.db.core import db_session
        with db_session() as session:
            user = User(username=username, password=password, is_superuser=True)
            session.add(user)
            session.commit()

            admin_role = session.query(Role).filter_by(code=str(ADMIN_ROLE['code'])).first()
            if admin_role:
                user_role = UserRole(user_id=user.id, role_id=admin_role.id)
                session.add(user_role)
            session.commit()
