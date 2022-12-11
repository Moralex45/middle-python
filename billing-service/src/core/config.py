from __future__ import annotations

import functools
from pathlib import Path

from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        __BASE_DIR_PATH = Path(__file__).parent.parent.parent
        __ENV_FILE_PATH = __BASE_DIR_PATH / '.env' / '.env.dev'

        env_file = __ENV_FILE_PATH
        env_file_encoding = 'utf-8'


class SentrySettings(BaseConfig):
    dsn: str = ''

    class Config:
        env_prefix = 'SENTRY_'


class ProjectSettings(BaseConfig):
    sentry_settings: SentrySettings = SentrySettings()

    project_name: str = 'Billing service'

    debug: bool = False


__settings = ProjectSettings()


@functools.lru_cache()
def get_settings() -> ProjectSettings:
    return __settings
