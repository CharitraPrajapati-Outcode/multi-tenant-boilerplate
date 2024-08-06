from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from apps.tenant.models import Company, Tenant, Domain


admin.site.register(Company)

@admin.register(Tenant)
class TenantAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'schema_name', 'is_active')
    search_fields = ('name', 'schema_name')
    list_filter = ('is_active',)


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'tenant', 'is_primary')
    search_fields = ('domain', 'tenant')
    list_filter = ('is_primary',)
