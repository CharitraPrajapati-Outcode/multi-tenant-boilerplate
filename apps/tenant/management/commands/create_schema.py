from django.conf import settings
from django.core.management import BaseCommand
from apps.tenant.models import Tenant, Domain


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        schema_name = input("Write the schema name: ")
        schema_full_name = input("Write the schema full name: ")
        tenant_domain = input("Write the tenant domain: ")
        is_primary = input("Is primary? (True/False): ")

        tenant = Tenant(schema_name=schema_name,  name=schema_full_name, is_active=True)
        tenant.save()

        domain = Domain()
        domain.domain = tenant_domain
        domain.tenant = tenant
        domain.is_primary = is_primary
        domain.save()

        print('Successfully loaded default schema!')
