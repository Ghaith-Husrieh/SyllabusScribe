from enum import Enum

from django.conf import settings
from guidance.models import LlamaCppChat
from llama_cpp import Llama

from decorators.log_decorators import log_function


class OperationResult(Enum):
    SUCCESS = 1
    FAILURE = 2
    MODEL_ALREADY_LOADED = 3


class LlamaInterface:
    llm = None

    @classmethod
    @log_function
    def load_model(cls):
        if cls.llm is None:
            try:
                cls.llm = Llama(model_path=str(settings.MODELS_ROOT / 'llama-2-7b-chat.Q8_0.gguf'),
                                n_ctx=4096, n_gpu_layers=32, verbose=True)
                return OperationResult.SUCCESS
            except Exception as e:
                return OperationResult.FAILURE
        else:
            return OperationResult.MODEL_ALREADY_LOADED

    @classmethod
    @log_function
    def create_local_instance(cls):
        if cls.llm is not None:
            return LlamaCppChat(model=cls.llm)
        else:
            return None
