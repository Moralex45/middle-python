from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django.core.signals import request_finished


class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'
    verbose_name = _('movies')

    def ready(self):
        import signals
        request_finished.connect(signals.new_filmwork_event)
