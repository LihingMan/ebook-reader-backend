from django.http import JsonResponse
from rest_framework import generics, mixins, status, views, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    ChangePasswordSerializer,
    CookieTokenRefreshSerializer,
    RegistrationSerializer,
)
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class RegisterUserView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return JsonResponse(
            data={"data": serializer.data},
            status=status.HTTP_201_CREATED,
        )


class CookieTokenObtainPairView(TokenObtainPairView):
    """Overrides default behaviour to set the refresh token in the httpOnly cookie"""

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            cookie_max_age = 3600 * 24 * 14  # set cookie expiry to 14 days

            # NOTE: in production set secure=True, so it can only be sent through HTTPS
            response.set_cookie(
                "refresh_token",
                response.data["refresh"],
                max_age=cookie_max_age,
                httponly=True,
            )
            del response.data["refresh"]
        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenRefreshView(TokenRefreshView):
    """Overrides default behaviour to set the refresh token in the httpOnly cookie"""

    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            cookie_max_age = 3600 * 24 * 14  # set cookie expiry to 14 days

            # NOTE: in production set secure=True, so it can only be sent through HTTPS
            response.set_cookie(
                "refresh_token",
                response.data["refresh"],
                max_age=cookie_max_age,
                httponly=True,
            )
            del response.data["refresh"]
        return super().finalize_response(request, response, *args, **kwargs)


class LogoutUserView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # if there is a need to add a feature to log out all user sessions
        # if self.request.data.get("all"):
        #     for token in OutstandingToken.objects.filter(user=request.user):
        #         _, _ = BlacklistedToken.objects.get_or_create(token=token)
        #         return Response(
        #             {"msg": "Successfully logged out. All refresh tokens for the user blacklisted"},
        #             status=status.HTTP_200_OK,
        #         )
        refresh_token = self.request.data.get("refresh")
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        return Response({"msg": "Successfully logged out."}, status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return JsonResponse(
            data={"msg": "Successfully changed password"}, status=status.HTTP_200_OK
        )
