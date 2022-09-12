import os
import sys

import uvicorn
from asgiref.wsgi import WsgiToAsgi

from main import create_app
from core.config import get_settings_instance
# from core.logger import LOGGING

SOURCE_DIR = os.path.dirname(__file__)
if SOURCE_DIR not in sys.path:
    sys.path.append(SOURCE_DIR)

asgi_app = WsgiToAsgi(create_app())


if __name__ == '__main__':
    uvicorn.run(
        'asgi:asgi_app',
        host=get_settings_instance().FLASK_HOST,
        port=get_settings_instance().FLASK_PORT,
        # log_config=LOGGING
    )