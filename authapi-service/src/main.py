import click
from flask import Flask

from core.config import get_settings_instance
from extentions import db
from models import *

__all__ = ('create_app',)

def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    configure_blueprints(app)
    configure_db(app)
    configure_cli(app)

    return app

def configure_db(app) -> None:
    app.config['SQLALCHEMY_DATABASE_URI'] = get_settings_instance().postgres_connection_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.app_context().push()
    db.create_all()

def configure_jwt():
    pass

def configure_blueprints(app) -> None:
    from api.v1.auth import blueprint as auth_blueprint
    from api.v1.role import blueprint as role_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(role_blueprint)

def configure_cli(app):
    @app.cli.command('createsuperuser')
    @click.argument('username')
    @click.argument('password')
    def create_superuser(username, password):
        pass