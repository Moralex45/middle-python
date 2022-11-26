import uuid
from json import dumps

import aiohttp
from src.core.config import get_settings


async def review_like_event(review_id: uuid.UUID):
    email_data = {
        'type': 'like',
        'sending_timeout': get_settings().notification_settings.email_timeout,
        'content': {
            'review_id': str(review_id),
        },
    }
    async with aiohttp.ClientSession() as session:
        await session.post(url=get_settings().notification_settings.url,
                           json=dumps(email_data),
                           headers='application/json')
