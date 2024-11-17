from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from . import views

urlpatterns = [
    path("signup/",view=views.SignUpView.as_view(),name="signup"),
    path("login/",view=views.LoginView.as_view(),name="login"),
    path("jwt/create/",view=TokenObtainPairView.as_view(),name="jwt_create"),
    path("jwt/refresh/",view=TokenRefreshView.as_view(),name="token_refresh/"),
    path("jwt/verify/",view=TokenVerifyView.as_view(),name="token_verify")
]