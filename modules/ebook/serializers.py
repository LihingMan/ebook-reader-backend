from django.contrib.auth import authenticate, user_logged_in
from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from .models import User
from django.contrib.auth.password_validation import validate_password
from utils.choices import Role
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50, min_length=6)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    name = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ["email", "password", "name"]

    def validate(self, attrs):
        email = attrs.get("email", None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": "Account with that email already exists"}
            )

        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_ebook_user(**validated_data)


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs["refresh"] = self.context["request"].COOKIES.get("refresh_token")
        if attrs["refresh"]:
            return super().validate(attrs)

        raise InvalidToken("No valid token found in cookie 'refresh_token'")


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ["email"]

    def validate_email(self, email):
        try:
            self.user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(["User not found"])

        return email


class ResetPasswordSerializer(serializers.ModelSerializer):
    token = serializers.CharField()

    class Meta:
        model = User
        fields = ["password", "token"]

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get("password"))
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["old_password", "new_password"]

    def validate_old_password(self, old_password):
        user = self.context.get("request").user

        if not check_password(old_password, user.password):
            raise serializers.ValidationError(["Wrong password"])

        return old_password

    def validate_new_pasword(self, new_password):
        validate_password(new_password, self.context.get("request").user)
        return new_password

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get("new_password"))
        instance.save()
        return instance
