from decorators.log_decorators import log_function
from llama_cpp import Llama
from django.conf import settings

llama2 = None


@log_function
def load_model():
    global llama2
    model_path = str(settings.MODELS_ROOT / 'llama-2-7b-chat.Q8_0.gguf')
    llama2 = Llama(model_path=model_path, n_ctx=4096, n_gpu_layers=32, verbose=True)
