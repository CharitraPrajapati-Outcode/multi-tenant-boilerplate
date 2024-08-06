For multi-tanent
https://django-tenants.readthedocs.io/en/latest/index.html

run ``` migrate_schemas --shared ```, this will create the shared apps on the public schema. Note: your database should be empty if this is the first time you’re running this command.

``` python manage.py migrate_schemas --shared ```

If you use migrate migrations will be applied to both shared and tenant schemas!

You might need to run ``` makemigrations ``` and then ``` migrate_schemas --shared ``` again for your app.Models to be created in the database.

For creating tenants

https://django-tenants.readthedocs.io/en/latest/use.html


schema_name_my = 'mercedes'
from django_tenants.utils import schema_context
with schema_context(schema_name_my):
    p1 = Plant.objects.create(name='Test', address='Test address')


To migrate specific schema
``` python manage.py migrate_schemas --schema second ```

migrate user roles on tenant
``` python manage.py tenant_command load_user_groups --schema=<schema_name> ```

create super admin for individual tenants
``` docker compose exec api python manage.py create_tenant_superuser --email=<email> --schema=<schema_name> ```



RUNNER_ALLOW_RUNASROOT="1"

Setup Project.
python manage.py load_default_schema
python manage.py createsuperuser

## Guide

### First time setup

1. Run `source ./entrypoint.sh` to setup the whole project.

### Running the project

1. Run `docker compose up` to start the project.

### Running the migrations

1. Run `docker compose exec api python manage.py migrate` to run the migrations.

### Creating a superuser

1. Run `docker compose exec api python manage.py createsuperuser` to create a superuser.

### Creating a tenant

1. Run `docker compose exec api python manage.py create_schema` to create a tenant.

### Removing a tenant

1. Run `docker compose exec api python manage.py delete_schema` to remove a tenant.


## References

- [Django Tenants](https://django-tenants.readthedocs.io/en/latest/index.html)