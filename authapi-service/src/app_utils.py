from flask import Flask

__all__ = ('create_app', 'create_raw_app')


def create_raw_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    configure_blueprints(app)

    return app


def create_app() -> Flask:
    app = create_raw_app()
    configure_db()
    # configure_cli(app)

    return app


def configure_db() -> None:
    from db.core import Base, engine
    from db.models.permissions import Permission, RolePermissions  # noqa
    from db.models.roles import Role, UserRole  # noqa
    from db.models.users import AuthHistory, User, UserData  # noqa
    Base.metadata.create_all(bind=engine)


def configure_jwt():
    pass


def configure_blueprints(app) -> None:
    from api.v1.auth import blueprint as auth_blueprint
    from api.v1.crud.role_permission import \
        blueprint as role_permission_blueprint
    from api.v1.crud.user_role import blueprint as user_role_blueprint
    from api.v1.role import blueprint as role_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(role_blueprint)
    app.register_blueprint(role_permission_blueprint)
    app.register_blueprint(user_role_blueprint)


def configure_cli(app):
    # @app.cli.command('createsuperuser')
    # @click.argument('username')
    # @click.argument('password')
    # def create_superuser(username, password):
    pass
