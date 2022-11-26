from requests import post
from json import dumps
from django.db.models.signals import post_save
from django.dispatch import receiver

from movies.models import FilmWork
from config.settings import NOTIFICATION_URL


@receiver(post_save, sender=FilmWork)
def new_filmwork_event(sender: FilmWork, **kwargs):
    if sender.created == sender.modified:
        event_dict = {
            'type': 'new_series',
            'content': {
                'movie_id': sender.id,
            },
        }
        post(NOTIFICATION_URL, json=dumps(event_dict), headers='application/json')
