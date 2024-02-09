from enum import Enum

from django.conf import settings
from joblib import load

from decorators.log_decorators import log_function


class OperationResult(Enum):
    SUCCESS = 1
    FAILURE = 2
    MODEL_ALREADY_LOADED = 3


class StudentPerformanceModelInterface:
    _model = None

    @classmethod
    @log_function
    def load_model(cls):
        if cls._model is None:
            try:
                cls._model = load(str(settings.MODELS_ROOT / 'student_performance_ML.joblib'))
                return OperationResult.SUCCESS
            except:
                return OperationResult.FAILURE
        else:
            return OperationResult.MODEL_ALREADY_LOADED

    @classmethod
    @log_function(log_result=False)
    def get_model(cls):
        return cls._model
