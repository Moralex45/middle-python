from flask import Flask

__all__ = ('create_app',)


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    configure_blueprints(app)
    configure_db()
    # configure_cli(app)

    return app


def configure_db() -> None:
    from db.models.users import User, UserData, AuthHistory  # noqa
    from db.models.roles import Role, UserRole  # noqa
    from db.models.permissions import Permission, RolePermissions  # noqa
    from db.core import Base, engine
    Base.metadata.create_all(bind=engine)


def configure_jwt():
    pass


def configure_blueprints(app) -> None:
    from api.v1.auth import blueprint as auth_blueprint
    from api.v1.role import blueprint as role_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(role_blueprint)


def configure_cli(app):
    # @app.cli.command('createsuperuser')
    # @click.argument('username')
    # @click.argument('password')
    # def create_superuser(username, password):
    pass
