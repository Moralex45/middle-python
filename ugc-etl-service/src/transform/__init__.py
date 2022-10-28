from json import loads

import pydantic

from models.view import View
from core.config import etl_logger


def transform_view(value_json: str):
    try:
        view = loads(value_json)
        return View(**view)
    except pydantic.ValidationError as e:
        etl_logger.error(e)
        return None
