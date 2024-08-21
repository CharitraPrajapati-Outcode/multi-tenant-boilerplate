# Project Title

**Description:**  
This project is a multi-tenant Django application using the `django-tenants` package. It supports multiple tenants, each with its own schema, while sharing certain apps across all tenants.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Project Setup](#project-setup)
3. [Running the Project](#running-the-project)
4. [Managing Tenants](#managing-tenants)
5. [References](#references)

## Getting Started

### Prerequisites

- Python 3.x
- Docker and Docker Compose
- PostgreSQL

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://your-repository-url.git
   cd your-project-directory
    ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
    ```

3. **Environment Configuration**
    ```bash
    cp .env.example .env
    ```

## Project Setup

### Initial Database Setup

1. **Run Initial Migrations**
    ```bash
    python manage.py migrate_schemas --shared
    ```

2. **Make Migrations for Your Apps**
    ```bash
    python manage.py makemigrations
    python manage.py migrate_schemas --shared
    ```

## Running the Project

### First Time Setup

    ```bash
    source ./entrypoint.sh
    ```

### Running the project

    ```bash
    Run `docker compose up` to start the project.
    ```

### Running the migrations

    ```bash
    Run `docker compose exec api python manage.py migrate` to run the migrations.
    ```

### Creating a superuser

    ```bash
    Run `docker compose exec api python manage.py createsuperuser` to create a superuser.
    ```

## Managing Tenants

### Creating a Tenant

1. **Create a Tenant**
    ```bash
    docker compose exec api python manage.py create_schema
    ```

2. **Remove a Tenant**
    ```bash
    docker compose exec api python manage.py delete_schema
    ```

3. **Creating a Super Admin for a Tenant**
    ```bash
    docker compose exec api python manage.py create_tenant_superuser --email=<email> --schema=<schema_name>
    ```

4. **Migrating Specific Schema**
    ```bash
    docker compose exec api python manage.py migrate_schemas --schema=<schema_name>
    ```

5. **Migrating User Roles on Tenant Schema**
    ```bash
    python manage.py tenant_command load_user_groups --schema=<schema_name>
    ```

6. **Creating Objects within a Specific Tenant**
    ```python
    from django_tenants.utils import schema_context

    schema_name_my = 'my-schema'
    with schema_context(schema_name_my):
        p1 = Plant.objects.create(name='Test', address='Test address')
    ```

## References

- [Django Tenants](https://django-tenants.readthedocs.io/en/latest/index.html)


## Extra

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
