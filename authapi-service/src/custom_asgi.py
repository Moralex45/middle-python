from gevent import monkey
monkey.patch_all()

from gevent.pywsgi import WSGIServer  # noqa
from app_utils import create_app # noqa
from core.config import get_settings_instance  # noqa


http_server = WSGIServer((get_settings_instance().FLASK_HOST, get_settings_instance().FLASK_PORT), create_app())
http_server.serve_forever()
