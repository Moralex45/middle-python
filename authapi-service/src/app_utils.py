from flask import Flask

__all__ = ('create_app', 'create_raw_app')


def create_raw_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    configure_blueprints(app)
    configure_jwt(app)

    return app


def create_app() -> Flask:
    app = create_raw_app()
    configure_db()
    # configure_cli(app)

    return app


def configure_db() -> None:
    from src.db.core import Base, engine
    from src.db.models.permissions import Permission, RolePermissions  # noqa
    from src.db.models.roles import Role, UserRole  # noqa
    from src.db.models.users import AuthHistory, User, UserData  # noqa
    Base.metadata.create_all(bind=engine)


def configure_jwt(app):
    from src.core.config import get_settings_instance

    app.config['JWT_SECRET_KEY'] = get_settings_instance().JWT_SECRET_KEY
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = get_settings_instance().JWT_ACCESS_TOKEN_EXPIRES
    app.config['JWT_COOKIE_SECURE'] = get_settings_instance().JWT_COOKIE_SECURE
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True
    app.config['JWT_ACCESS_CSRF_HEADER_NAME'] = "X-CSRF-TOKEN-ACCESS"

    from flask_jwt_extended import JWTManager
    jwt = JWTManager(app)

    from src.db.services.user import UserService
    from src.db.services.user_role import UserRoleService
    from src.db.services.role import RoleService
    from src.db.services.role_permission import RolePermissionService

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return UserService.get_by_id(identity)

    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity):
        users_roles = UserRoleService.get_filtered(identity.id)
        return {
            "iss": get_settings_instance().PROJECT_NAME,
            "permissions": [],
            "is_super": True,
            "aud": "some_audience",
            "foo": "bar",
            "upcase_name": '',
        }


def configure_blueprints(app) -> None:
    from src.api.v1.auth.register import blueprint as register_blueprint
    from src.api.v1.auth.login import blueprint as login_blueprint
    from src.api.v1.crud.role_permission import \
        blueprint as role_permission_blueprint
    from src.api.v1.crud.user_role import blueprint as user_role_blueprint
    from src.api.v1.role import blueprint as role_blueprint
    app.register_blueprint(role_blueprint)
    app.register_blueprint(role_permission_blueprint)
    app.register_blueprint(user_role_blueprint)
    app.register_blueprint(register_blueprint)
    app.register_blueprint(login_blueprint)


def configure_cli(app):
    # @app.cli.command('createsuperuser')
    # @click.argument('username')
    # @click.argument('password')
    # def create_superuser(username, password):
    pass
