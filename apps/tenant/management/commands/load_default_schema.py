from django.conf import settings
from django.core.management import BaseCommand
from apps.tenant.models import Tenant, Domain


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        tenant = Tenant(schema_name='public',  name='My Project', is_active=True)
        tenant.save()

        domain = Domain()
        domain.domain = settings.DOMAIN
        domain.tenant = tenant
        domain.is_primary = True
        domain.save()

        print('Successfully loaded default schema!')
