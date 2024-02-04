from django.apps import AppConfig


class BugtrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bugtracker'

    def ready(self):
        from . import signals
