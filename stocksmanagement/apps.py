from django.apps import AppConfig


class StocksmanagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stocksmanagement'

    def ready(self):
        import stocksmanagement.signals
