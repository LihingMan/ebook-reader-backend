from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import (
    CookieTokenObtainPairView,
    CookieTokenRefreshView,
    LogoutUserView,
    RegisterUserView,
    ChangePasswordView,
)

urlpatterns = [
    # path("login/", TokenObtainPairView.as_view(), name="login"),
    # path("refresh-token/", TokenRefreshView.as_view(), name="token_refresh"),
    path("login/", CookieTokenObtainPairView.as_view(), name="login"),
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path("refresh-token/", CookieTokenRefreshView.as_view(), name="token_refresh"),
    path("token-verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("register/", RegisterUserView.as_view(), name="register"),
    path("change-password/", view=ChangePasswordView.as_view(), name="change-password"),
]
