from django.apps import AppConfig
from .utils.model_loader import load_model


class StudentperformancemodelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'StudentPerformanceModel'

    def ready(self):
        load_model()
