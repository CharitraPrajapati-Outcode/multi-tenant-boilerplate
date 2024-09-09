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

## Prerequisites

- Docker and Docker Compose installed on your local machine
- Git
- AWS account (for deployment)
- Python 3.8+ (for running the app locally without Docker)

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://your-repo-url.git
    cd your-repo-name
    ```

2. **Set Up Environment Variables**

   Create a `.env` file in the project root with the necessary environment variables:

    ```plaintext
    DEBUG=True
    SECRET_KEY=your_secret_key
    POSTGRES_DB=project_db
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=admin
    ALLOWED_HOSTS=localhost,127.0.0.1
    ```

3. **Build and Start the Containers**

    ```bash
    docker-compose up --build
    ```

4. **Initiate the Database**

    ```bash
    docker-compose exec db createdb -U postgres project_db
    ```

5. **Load default schema, Apply Migrations and Create Superuser**

    ```bash
    docker-compose exec api python manage.py load_default_schema
    docker-compose exec api python manage.py migrate
    docker-compose exec api python manage.py createsuperuser
    ```

6. **Collect Static Files**

    ```bash
    docker-compose exec api python manage.py collectstatic --noinput
    ```

7. **Load default data**

    ```bash
    docker compose -f ./docker-compose.stage.yml exec api python manage.py load_super_admin
    ```

8. **Migrate specific schema**

    ```bash
    docker-compose exec api python manage.py migrate _schemas --schema <schema_name>
    ```

9. **Migrate shared schema**

    ```bash
    docker-compose exec api python manage.py migrate_schemas --schema shared
    ```

## Running the Application

The application is accessible via `http://localhost:8000` after running the Docker containers. You can access the admin panel at `http://localhost:8000/admin` with the superuser credentials.

- **API Documentation**: Available via the DRF browsable API interface. `http://localhost:8000/api/swagger/`
- **Mailhog Interface**: Accessible via `http://localhost:8025` for testing emails.


## Running the Project

### First Time Setup

    ```bash
    source ./entrypoint.sh
    ```


## Testing

To run the test suite, use the following command:

```bash
docker-compose exec api python manage.py test
```

To run specific tests, run the following command

```bash
docker compose exec api python manage.py test apps.<app_name>.tests.<test_file_name>
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

3. **List all Tenants**
    ```bash
    docker compose exec api python manage.py list_schemas
    ```

4. **Creating a Super Admin for a Tenant**
    ```bash
    docker compose exec api python manage.py create_tenant_superuser --email=<email> --schema=<schema_name>
    ```

5. **Migrating Specific Schema**
    ```bash
    docker compose exec api python manage.py migrate_schemas --schema=<schema_name>
    ```

6. **Migrating User Roles on Tenant Schema**
    ```bash
    python manage.py tenant_command load_user_groups --schema=<schema_name>
    ```

7. **Creating Objects within a Specific Tenant**
    ```python
    from django_tenants.utils import schema_context

    schema_name_my = 'my-schema'
    with schema_context(schema_name_my):
        p1 = Plant.objects.create(name='Test', address='Test address')
    ```

## References

- [Django Tenants](https://django-tenants.readthedocs.io/en/latest/index.html)


## Additional Information

For multi-tanent
https://django-tenants.readthedocs.io/en/latest/index.html

run ``` migrate_schemas --shared ```, this will create the shared apps on the public schema. Note: your database should be empty if this is the first time you’re running this command.

``` python manage.py migrate_schemas --shared ```

If you use migrate migrations will be applied to both shared and tenant schemas!

You might need to run ``` makemigrations ``` and then ``` migrate_schemas --shared ``` again for your app.Models to be created in the database.

For creating tenants

https://django-tenants.readthedocs.io/en/latest/use.html


```python
schema_name_my = 'test'
from django_tenants.utils import schema_context
with schema_context(schema_name_my):
    p1 = Address.objects.create(name='Test', address='Test address')
```
