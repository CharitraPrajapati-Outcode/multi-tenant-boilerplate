import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.validators import ASCII_USERNAME_VALIDATOR


class Company(models.Model):
    id = models.UUIDField(
        max_length=150,
        primary_key=True,
        unique=True,
        error_messages={
            'unique': "Company with the uid already exists",
        },
        default=uuid.uuid4
    )
    name = models.CharField(_('name'), 
            max_length=32, 
            unique=True,
            error_messages={
                    'unique': "Company name already exists",
                } 
            )
    company_tenant = models.CharField(_('company_tenant'), 
                max_length=16, 
                validators=[ASCII_USERNAME_VALIDATOR], 
                unique=True,
                error_messages={
                    'unique': "Company tenant already exists",
                }
                )
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated_at'), auto_now=True)