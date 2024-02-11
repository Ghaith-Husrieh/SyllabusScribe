from enum import Enum

import pandas as pd
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
    def predict_performance_index(cls, hours_studied, previous_score, extracurricular_activities, sleep_hours, sample_question_papers_practiced):
        model_input = pd.DataFrame(
            [[
                hours_studied,
                previous_score,
                extracurricular_activities,
                sleep_hours,
                sample_question_papers_practiced
            ]],
            columns=['Hours Studied', 'Previous Scores', 'Extracurricular Activities',
                     'Sleep Hours', 'Sample Question Papers Practiced']
        )
        return cls._model.predict(model_input)

    @classmethod
    @log_function(log_result=False)
    def is_loaded(cls):
        if cls._model is not None:
            return True
        else:
            return False
