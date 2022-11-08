"""Django settings for config project."""

import os
from pathlib import Path
from dotenv import load_dotenv
from split_settings.tools import include

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


# Load local .env file
ENV_DIR_FILE_PATH = Path(__file__).parent.parent.parent / '.env'
load_dotenv(ENV_DIR_FILE_PATH / '.env.dev')

# Include additional settings
include(
    'components/database.py',
    'components/application.py',
    'components/localization.py',
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = os.environ.get('DEBUG', False) == 'True'

ALLOWED_HOSTS = ['127.0.0.1']

INTERNAL_IPS = ['127.0.0.1']

LOCALE_PATHS = ['movies/locale']

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Static files (CSS, JavaScript, Images)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = 'static/'
STATIC_ROOT = Path(BASE_DIR).joinpath('static')
MEDIA_URL = 'media/'
MEDIA_ROOT = Path(BASE_DIR).joinpath('media')
STATICFILES_DIRS = []

# Debug logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
        },
    },
    'handlers': {
        'debug-console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'filters': ['require_debug_true'],
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['debug-console'],
            'propagate': False,
        },
    },
}

# DRF Settings
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50,
}

if DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append('rest_framework.renderers.BrowsableAPIRenderer')

# URL Swagger UI
CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:8080',
]

if not DEBUG:
    sentry_sdk.init(integrations=[DjangoIntegration()])
