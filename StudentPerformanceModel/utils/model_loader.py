from decorators.log_decorators import log_function
from joblib import load
from django.conf import settings

student_performance_model = None


@log_function
def load_model():
    global student_performance_model
    model_path = str(settings.MODELS_ROOT / 'student_performance_ML.joblib')
    student_performance_model = load(model_path)
