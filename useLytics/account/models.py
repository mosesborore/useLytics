from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _

from account.utils import normalize_phone


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(
        db_column="User_id",
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID",
    )
    name = models.CharField(
        max_length=255, blank=True, null=True, db_column="User_name"
    )
    phone_number = models.CharField(
        _("User Phone Number"),
        max_length=12,
        blank=True,
        default="",
        null=True,
        db_column="User_phone_number",
        unique=True,
    )
    email = models.EmailField(
        _("Email"), max_length=254, db_column="User_email", unique=True
    )
    password = models.CharField(
        _("password"), max_length=128, db_column="User_password", blank=True, default=""
    )
    is_staff = models.BooleanField("Is staff", db_column="User_is_staff", default=False)
    is_superuser = models.BooleanField(
        "Is superuser", db_column="User_is_superuser", default=False
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
        db_column="User_is_active",
    )
    last_login = models.DateTimeField("last login", null=True, auto_now=True)

    created_at = models.DateTimeField(
        "Created at",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        "Updated at",
        auto_now=True,
    )

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    class Meta:
        db_table = "Users"
        ordering = ("phone_number",)

    def __str__(self):
        return str(f"User: {self.id} - {self.email}")

    def get_full_name(self):
        return self.name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def save(self, *args, **kwargs):
        parsed_phone_number = normalize_phone(self.phone_number)
        if not self.phone_number == parsed_phone_number:
            self.phone_number = parsed_phone_number
        super().save(*args, **kwargs)
