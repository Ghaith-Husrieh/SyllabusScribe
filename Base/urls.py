from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from . import views

urlpatterns = [
    path('auth/signup/', views.signup, name='signup'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/login/refresh', TokenRefreshView.as_view(), name='login-refresh'),
    path('user/personal-info', views.get_personal_info, name='get_user_info'),
    path('user/subjects', views.get_user_subjects, name='get_user_subjects'),
    path('user/lesson-plans', views.get_user_lesson_plans, name='get_user_lesson_plans'),
    path('user/lesson-contexts', views.get_user_lesson_contexts, name='get_user_lesson_contexts'),
    path('user/lesson-presentations', views.get_user_lesson_presentations, name='get_user_lesson_presentations'),
    path('user/lesson-handouts', views.get_user_lesson_handouts, name='get_user_lesson_handouts'),
    path('user/lesson-quizzes', views.get_user_lesson_quizzes, name='get_user_lesson_quizzes')
]
