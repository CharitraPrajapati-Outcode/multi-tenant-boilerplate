import datetime
import uuid

from django.utils import timezone
from django.conf import settings
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property

from apps.core.validators import USERNAME_VALIDATOR
from ..manager import UserManager


class LowerCaseEmailAddressField(models.EmailField):
    def get_prep_value(self, value):
        return str(value).lower()


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        max_length=150,
        primary_key=True,
        unique=True,
        validators=[USERNAME_VALIDATOR],
        error_messages={
            'unique': "User with the uid already exists",
        },
        default=uuid.uuid4
    )
    email = LowerCaseEmailAddressField(_('email'), unique=True)
    first_name = models.CharField(_('first_name'), max_length=60, blank=True)
    last_name = models.CharField(_('last_name'), max_length=60, blank=True)
    is_staff = models.BooleanField(_('is_staff'), default=False)
    is_deleted = models.BooleanField(_('is_deleted'), default=False)
    deleted_at = models.DateTimeField(_('deleted_at'), default=None, null=True)
    is_verified = models.BooleanField(_('is_verified'), default=False)
    is_active = models.BooleanField(_('is_active'), default=False)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated_at'), auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = datetime.datetime.now()
        self.save()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images', null=True, blank=True)

    class Meta:
        db_table = "user_profile"
        verbose_name = "user_profile"
        verbose_name_plural = "user_profiles"

    def __str__(self):
        return self.first_name + " " + self.last_name
