from django.apps import AppConfig

from .utils.llama_interface import LlamaInterface


class LargelanguagemodelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'LargeLanguageModel'

    def ready(self):
        LlamaInterface.load_model()
