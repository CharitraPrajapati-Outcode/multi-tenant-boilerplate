from django_tenants.middleware.main import TenantMainMiddleware
from django.urls import set_urlconf
from django.http import Http404
from django.db import connection
from django_tenants.utils import get_tenant_model, get_public_schema_name


class TenantMiddleware(TenantMainMiddleware):
    """
    Field is_active can be used to temporary disable tenant and
    block access to their site. Modifying get_tenant method from
    TenantMiddleware allows us to check if tenant should be available
    """
    def process_request(self, request):
        schema_name = request.headers.get('X-Schema-Name')

        if schema_name:
            connection.set_schema_to_public()

            TenantModel = get_tenant_model()
            try:
                tenant = TenantModel.objects.get(schema_name=schema_name)
            except TenantModel.DoesNotExist:
                raise Http404("Tenant does not exist")

            request.tenant = tenant
            connection.set_tenant(request.tenant)

            if connection.schema_name != get_public_schema_name():
                connection.set_schema(schema_name)
        else:
            if '/admin' in request.path:
                domain_parts = request.get_host().split('.')
                if len(domain_parts) == 1:
                    connection.set_schema_to_public()
                if len(domain_parts) == 2:
                    schema_name = domain_parts[0]  

                    connection.set_schema_to_public()

                    TenantModel = get_tenant_model()
                    try:
                        tenant = TenantModel.objects.get(schema_name=schema_name)
                    except TenantModel.DoesNotExist:
                        raise Http404("Tenant does not exist")

                    request.tenant = tenant
                    connection.set_tenant(request.tenant)

                    if connection.schema_name != get_public_schema_name():
                        connection.set_schema(schema_name)
                        # connection.set_schema_to_public()
