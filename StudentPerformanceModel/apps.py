from django.apps import AppConfig

from .utils.student_performance_model_interface import \
    StudentPerformanceModelInterface


class StudentperformancemodelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'StudentPerformanceModel'

    def ready(self):
        StudentPerformanceModelInterface.load_model()
