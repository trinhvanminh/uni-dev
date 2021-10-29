from django.apps import AppConfig


class IobDemoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'iob_demo'

    def ready(self):
        import iob_demo.signals
