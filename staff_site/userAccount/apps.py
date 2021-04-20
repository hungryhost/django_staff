from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'userAccount'

    def ready(self):
        """Initializes signals.
        """
        from . import signals
        return True
