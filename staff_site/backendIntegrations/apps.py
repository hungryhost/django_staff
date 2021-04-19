from django.apps import AppConfig


class BackendintegrationsConfig(AppConfig):
    name = 'backendIntegrations'

    def ready(self):
        """Initializes signals.
        """
        from . import signals
        return True