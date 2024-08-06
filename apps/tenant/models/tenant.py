from django.db import models
from django.utils.translation import gettext_lazy as _
from django_tenants.models import TenantMixin, DomainMixin


class Tenant(TenantMixin):
    name = models.CharField(_('name'), max_length=32)
    is_active = models.BooleanField(_('is_active'), default=True)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated_at'), auto_now=True)

    auto_create_schema = True

    
class Domain(DomainMixin):
    pass