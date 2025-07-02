from django.apps import AppConfig


class BackofficeEngineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backoffice_engine'

    def ready(self):
        import backoffice_engine.signals