from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.conf import settings

from .models import Company, Tenant, Domain


@staticmethod
@receiver(post_save, sender=Company)
def create_tenant(sender, instance, created, **kwargs):
    if created:
        
        tenant = Tenant(schema_name=instance.company_tenant,  name=instance.name, is_active=True)
        tenant.save()
        
        domain = Domain()
        domain.domain = instance.company_tenant + '.' + settings.DOMAIN
        domain.tenant = tenant
        domain.is_primary = True
        domain.save()