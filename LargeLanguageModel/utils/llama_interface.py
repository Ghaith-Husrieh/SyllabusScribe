from enum import Enum

from colorama import Fore
from django.conf import settings
from guidance.models import LlamaCppChat
from llama_cpp import Llama

from decorators.log_decorators import log_function


class OperationResult(Enum):
    SUCCESS = 1
    FAILURE = 2
    MODEL_ALREADY_LOADED = 3


class LlamaInterface:
    _llm = None

    @classmethod
    @log_function
    def load_model(cls, context_length=4096, layers_to_offload=32, verbose=True):
        if cls._llm is None:
            try:
                if context_length > 4096:
                    print(
                        Fore.YELLOW
                        + f"Warning: Provided 'context_length' value ({context_length}) exceeds the maximum allowable length for the model.\nTherefore, the context length has been adjusted to the maximum allowable value of 4096."
                        + Fore.RESET
                    )
                    context_length = 4096
                if layers_to_offload > 35:
                    print(
                        Fore.YELLOW
                        + f"Warning: Specified 'layers_to_offload' value ({layers_to_offload}) exceeds the maximum allowable number of layers for offloading, which is 35.\nTherefore, The value has been adjusted to the maximum allowable value of 35."
                        + Fore.RESET
                    )
                    layers_to_offload = 35
                cls._llm = Llama(model_path=str(settings.MODELS_ROOT / 'llama-2-7b-chat.Q8_0.gguf'),
                                 n_ctx=context_length, n_gpu_layers=layers_to_offload, verbose=verbose)
                return OperationResult.SUCCESS
            except:
                return OperationResult.FAILURE
        else:
            return OperationResult.MODEL_ALREADY_LOADED

    @classmethod
    @log_function(log_result=False)
    def create_local_instance(cls):
        if cls._llm is not None:
            return LlamaCppChat(model=cls._llm)
        else:
            return None
