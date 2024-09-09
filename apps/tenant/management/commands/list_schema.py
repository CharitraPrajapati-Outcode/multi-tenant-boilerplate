from django.conf import settings
from django.core.management import BaseCommand
from apps.tenant.models import Tenant, Domain


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        available_schemas = Tenant.objects.all()
        print('Available schemas:')
        for schema in available_schemas:
            print(schema.schema_name)
        print('Successfully listed schemas!')
