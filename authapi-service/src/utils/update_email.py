import hashlib
from json import dumps

from requests import post
import uuid

from src.core.config import get_settings_instance
from src.db.models.users import PasswordConstants
from src import cache


def UpdateEmail(user_id: uuid.UUID, email: str):
    confirm_url_param = str(user_id) + email
    confirm_url_param = hashlib.pbkdf2_hmac(
        PasswordConstants.algorithm,
        confirm_url_param.encode('utf-8'),
        get_settings_instance.CONFIRM_URL_SALT,
        PasswordConstants.iterations,
    )
    cache.cache_service.set(key=confirm_url_param, value='VALID', expire=get_settings_instance().CONFIRM_URL_EXPIRED)
    conf_url = get_settings_instance().SITE_URL + '/api/v1/crud/user/' + str(user_id) + '/?confirm=' + confirm_url_param
    email_data = {
        'type': 'registartion',
        'content': {
            'user_id': str(user_id),
            'conf_url': conf_url,
        },
    }
    post(get_settings_instance().NOTIFICATION_URL, json=dumps(email_data), headers='application/json')
