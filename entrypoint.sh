#!/bin/bash

# Build application
docker compose build

# Run application in background
docker compose up -d

# Create database named project_db if not exists
# docker compose exec db psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'project_db'" | grep -q 1 || docker compose exec db psql -U postgres -c "CREATE DATABASE project_db;"

# Make migrations
docker compose exec api python manage.py makemigrations

# Migrate the database
docker compose exec api python manage.py migrate_schemas --shared

# Collect static files
# docker compose exec api python manage.py collectstatic --noinput

# Load default schema
docker compose exec api python manage.py load_default_schema

# Create super user
# docker compose exec api python manage.py createsuperuser
