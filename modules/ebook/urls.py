from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenVerifyView,
)
from rest_framework.routers import DefaultRouter
from .auth_views import (
    CookieTokenObtainPairView,
    CookieTokenRefreshView,
    LogoutUserView,
    RegisterUserView,
    ChangePasswordView,
)
from .core_views import RetrieveListEbookViewSet, UploadEbookView

router = DefaultRouter()


router.register(r"ebook-r", RetrieveListEbookViewSet, basename="ebook-r")

urlpatterns = [
    path("", include(router.urls)),
    # path("login/", TokenObtainPairView.as_view(), name="login"),
    # path("refresh-token/", TokenRefreshView.as_view(), name="token_refresh"),
    path("login/", CookieTokenObtainPairView.as_view(), name="login"),
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path("refresh-token/", CookieTokenRefreshView.as_view(), name="token_refresh"),
    path("token-verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("register/", RegisterUserView.as_view(), name="register"),
    path("change-password/", view=ChangePasswordView.as_view(), name="change-password"),
    path("ebook-c/", view=UploadEbookView.as_view(), name="ebook-c"),
]
