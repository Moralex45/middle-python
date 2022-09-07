"""Django database connection settings config."""

import os

DEFAULT_DB_HOST = '127.0.0.1'
DEFAULT_DB_PORT = 5432


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', DEFAULT_DB_HOST),
        'PORT': os.environ.get('DB_PORT', DEFAULT_DB_PORT),
        'OPTIONS': {
            'options': '-c search_path=public,content'
        }
    }
}

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
