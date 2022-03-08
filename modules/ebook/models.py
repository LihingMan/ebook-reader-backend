from tabnanny import verbose
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    Group as DjangoGroup,
)
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from utils.choices import Role


class UserManager(BaseUserManager):
    def _create_user(self, email, password, name, role):
        if not email:
            raise ValueError("Users must have an email")
        if not password:
            raise ValueError("Users must have a password")
        if not name:
            raise ValueError("Users must have a name")
        if not role:
            raise ValueError("Users must have a role")

        user = self.model(email=email, name=name, role=role)
        user.set_password(password)
        user.save(using=self.db)
        try:
            pass
        except:
            pass

        try:
            DjangoGroup.objects.get(name=role).user_set.add(user)
        except:
            print(role)

        return user

    def create_ebook_user(self, email, password, name):
        return self._create_user(email, password, name, Role.USER)

    def create_ebook_superuser(self, email, password, name):
        return self._create_user(email, password, name, Role.SUPERUSER)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        max_length=255,
        validators=[
            RegexValidator(regex=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
        ],
        verbose_name="Email",
    )
    name = models.CharField(max_length=255, verbose_name="Name")
    role = models.CharField(max_length=2, choices=Role.CHOICES, verbose_name="Role")
    is_active = models.BooleanField(default=True, verbose_name="User account is active")
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Time create")
    time_updated = models.DateTimeField(auto_now=True, verbose_name="Time updated")

    USERNAME_FIELD = "email"
    objects = UserManager()

    def _check_role(self, role):
        return self.role == role

    @property
    def is_superuser(self):
        return self._check_role(Role.SUPERUSER)

    @property
    def is_user(self):
        return self._check_role(Role.USER)
