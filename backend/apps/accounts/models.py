from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.contrib import auth
from django.apps import apps
from django.db import models
from django.forms import ValidationError
from django.core.mail import send_mail

class AuthUserManager(BaseUserManager):

    def _create_user(self, username, email, password, **extra_fields):

        if not username:
            raise ValueError("You have to set valid username")
        
        if not email:
            raise ValueError("You have to set valid email adress")
        
        email = self.normalize_email(email)

        if self.filter(email=email):
            raise ValidationError("Provided email already exists in database")

        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save()

        return user
    
    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)

    def with_perm(
        self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()

class AuthUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=150, unique=True, error_messages={
            "unique": "A user with that username already exists.",
        },)
    email = models.EmailField(unique=True, error_messages={
            "unique": "A user with that email already exists.",
        },)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_created = models.DateField(auto_now_add=True)

    objects = AuthUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def _generate_jwt(self):
        pass

    class Meta(AbstractBaseUser.Meta):
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

