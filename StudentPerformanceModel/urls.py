from django.urls import path
from . import views


urlpatterns = [
    path('query/', views.student_performance_model_query, name='student_performance_query'),
]
