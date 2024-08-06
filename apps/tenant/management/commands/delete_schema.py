from django.conf import settings
from django.core.management import BaseCommand
from apps.tenant.models import Tenant, Domain


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        schema_name = input("Write the schema name: ")
        schema_full_name = input("Write the schema full name: ")
        tenant_domain = input("Write the tenant domain: ")
        is_primary = input("Is primary? (True/False): ")

        # delete the schema
        try:
            tenant = Tenant.objects.get(schema_name=schema_name)
            tenant.delete()

            domain = Domain.objects.get(domain=tenant_domain)
            domain.delete()

            print('Successfully deleted schema!')
        except Tenant.DoesNotExist:
            print('Schema does not exist!')
        except Domain.DoesNotExist:
            print('Domain does not exist!')
