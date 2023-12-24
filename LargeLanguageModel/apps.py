from django.apps import AppConfig
from .utils.model_loader import load_model


class LargelanguagemodelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'LargeLanguageModel'

    def ready(self):
        load_model()
