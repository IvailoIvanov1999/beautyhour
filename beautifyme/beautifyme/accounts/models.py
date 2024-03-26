import os

from django.contrib.auth.hashers import make_password
from django.core.validators import MinValueValidator
from django.db import models

from django.utils.translation import gettext_lazy as _
from django.contrib.auth import models as auth_models

from django.utils import timezone

from beautifyme.accounts.managers import BeautyHourUserManager


def profile_image_upload_path(instance, filename):
    basefilename, extension = os.path.splitext(filename)
    first_name = instance.first_name.replace(" ", "_")
    last_name = instance.last_name.replace(" ", "_")

    return f'media/profile_pictures/{first_name}_{last_name}/{basefilename}{extension}'


class BeautyHourUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    is_staff = models.BooleanField(
        default=False,
    )

    is_superuser = models.BooleanField(default=False)

    is_active = models.BooleanField(
        default=True,
    )

    USERNAME_FIELD = "email"

    objects = BeautyHourUserManager()


class Profile(models.Model):
    MAX_FIRST_NAME_LENGTH = 30
    MAX_LAST_NAME_LENGTH = 30

    first_name = models.CharField(
        max_length=MAX_FIRST_NAME_LENGTH,
        blank=True,
        null=True,
    )

    last_name = models.CharField(
        max_length=MAX_LAST_NAME_LENGTH,
        blank=True,
        null=True,
    )

    profile_picture = models.ImageField(upload_to=profile_image_upload_path, null=True, blank=True)

    date_of_birth = models.DateField(null=True, blank=True)

    user = models.OneToOneField(
        BeautyHourUser,
        primary_key=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.user.email

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'

        return self.first_name or self.last_name
