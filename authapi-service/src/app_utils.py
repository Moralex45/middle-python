import click
from flask import Flask

from src.core.config import get_settings_instance
from src.core.extentions import init_oauth
from src.core.tracer import init_tracer

__all__ = ('create_app', 'create_raw_app')


def create_raw_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    configure_blueprints(app)
    configure_jwt(app)
    configure_cache()

    return app


def create_app() -> Flask:
    app = create_raw_app()
    configure_db()
    configure_cli(app)
    init_oauth(app)
    if get_settings_instance().ENABLE_TRACER:
        init_tracer(app)

    return app


def configure_db() -> None:
    from src.db.core import Base, engine
    from src.db.models.permissions import Permission, RolePermissions  # noqa
    from src.db.models.roles import Role, UserRole  # noqa
    from src.db.models.social_account import SocialAccount  # noqa
    from src.db.models.users import AuthHistory, User, UserData  # noqa
    Base.metadata.create_all(bind=engine)


def configure_cache():
    import redis

    from src import cache
    from src.cache.redis import RedisCacheService
    from src.core.config import get_settings_instance

    redis_instance = redis.Redis(host=get_settings_instance().REDIS_HOST,
                                 port=get_settings_instance().REDIS_PORT,
                                 decode_responses=True)
    cache.cache_service = RedisCacheService(redis_instance)


def configure_jwt(app):
    from src.core.config import get_settings_instance

    app.config['SECRET_KEY'] = get_settings_instance().APP_SECRET_KEY
    app.config['JWT_SECRET_KEY'] = get_settings_instance().JWT_SECRET_KEY
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = get_settings_instance().JWT_ACCESS_TOKEN_EXPIRES
    app.config['JWT_COOKIE_SECURE'] = get_settings_instance().JWT_COOKIE_SECURE
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False

    from flask_jwt_extended import JWTManager

    jwt = JWTManager(app)

    from src.db.services.permissions import PermissionService
    from src.db.services.user import UserService

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data['sub']
        return UserService.get_by_id(identity)

    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity):
        user_permissions = PermissionService.get_filtered_by_user_id(identity.id)
        return {
            'iss': get_settings_instance().PROJECT_NAME,
            'permissions': [user_permission.code for user_permission in user_permissions],
            'is_super': identity.is_superuser,
        }


def configure_blueprints(app) -> None:
    from src.api.v1.auth.login import blueprint as login_blueprint
    from src.api.v1.auth.logout import blueprint as logout_blueprint
    from src.api.v1.auth.refresh import blueprint as refresh_blueprint
    from src.api.v1.auth.register import blueprint as register_blueprint
    from src.api.v1.crud.permission import blueprint as permission_blueprint
    from src.api.v1.crud.role import blueprint as role_blueprint
    from src.api.v1.crud.role_permission import \
        blueprint as role_permission_blueprint
    from src.api.v1.crud.user import blueprint as user_blueprint
    from src.api.v1.crud.user_role import blueprint as user_role_blueprint
    from src.api.v1.oauth.oauth_routes import blueprint as oauth_blueprint

    app.register_blueprint(role_blueprint)
    app.register_blueprint(permission_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(role_permission_blueprint)
    app.register_blueprint(user_role_blueprint)
    app.register_blueprint(register_blueprint)
    app.register_blueprint(login_blueprint)
    app.register_blueprint(logout_blueprint)
    app.register_blueprint(refresh_blueprint)
    app.register_blueprint(oauth_blueprint)


def configure_cli(app):
    @app.cli.command('createdatabase')
    def create_database():
        configure_db()

    @app.cli.command('createdefault')
    def create_default_data():
        from src.core.constants import (ADMIN_ROLE, CAN_ACCESS_PERMISSION,
                                        CAN_ACCESS_ROLE,
                                        CAN_ACCESS_ROLE_PERMISSION,
                                        CAN_ACCESS_USER_ROLE, CAN_EDIT_PROFILE,
                                        SAMPLE_USER_ROLE)
        from src.db.core import db_session
        from src.db.models.permissions import Permission, RolePermissions
        from src.db.models.roles import Role

        with db_session() as session:
            db_role_admin = Role(
                **ADMIN_ROLE,
            )

            db_role_user = Role(
                **SAMPLE_USER_ROLE,
            )

            db_can_add_role = Permission(
                **CAN_ACCESS_ROLE,
            )

            db_can_add_permission = Permission(
                **CAN_ACCESS_PERMISSION,
            )

            db_can_add_role_permission = Permission(
                **CAN_ACCESS_ROLE_PERMISSION,
            )

            db_can_add_user_role = Permission(
                **CAN_ACCESS_USER_ROLE,
            )

            db_can_edit_profile = Permission(
                **CAN_EDIT_PROFILE,
            )

            session.add_all(
                [
                    db_role_admin,
                    db_role_user,
                    db_can_add_role,
                    db_can_add_permission,
                    db_can_add_role_permission,
                    db_can_add_user_role,
                    db_can_edit_profile,
                ],
            )
            session.commit()

            role_admin_can_add_role = RolePermissions(
                role_id=db_role_admin.id,
                perm_id=db_can_add_role.id,
            )
            role_admin_can_add_permission = RolePermissions(
                role_id=db_role_admin.id,
                perm_id=db_can_add_permission.id,
            )
            role_admin_can_add_role_permission = RolePermissions(
                role_id=db_role_admin.id,
                perm_id=db_can_add_role_permission.id,
            )
            role_admin_can_add_user_role = RolePermissions(
                role_id=db_role_admin.id,
                perm_id=db_can_add_user_role.id,
            )
            role_sample_user_can_edit_profile = RolePermissions(
                role_id=db_role_user.id,
                perm_id=db_can_edit_profile.id,
            )

            session.add_all(
                [
                    role_admin_can_add_role,
                    role_admin_can_add_permission,
                    role_admin_can_add_role_permission,
                    role_admin_can_add_user_role,
                    role_sample_user_can_edit_profile,
                ],
            )
            session.commit()

    @app.cli.command('createsuperuser')
    @click.argument('username')
    @click.argument('password')
    def create_superuser(username, password):
        from src.core.constants import ADMIN_ROLE
        from src.db.core import db_session
        from src.db.models.roles import Role, UserRole
        from src.db.models.users import User
        with db_session() as session:
            user = User(username=username, password=password, is_superuser=True)
            session.add(user)
            session.commit()

            admin_role = session.query(Role).filter_by(code=str(ADMIN_ROLE['code'])).first()
            if admin_role:
                user_role = UserRole(user_id=user.id, role_id=admin_role.id)
                session.add(user_role)
            session.commit()
