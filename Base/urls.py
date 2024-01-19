from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from . import views

urlpatterns = [
    path('auth/signup/', views.signup, name='signup'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/login/refresh', TokenRefreshView.as_view(), name='login-refresh')
]
