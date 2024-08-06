#!/bin/bash

# Build application
docker compose build

# Run application in background
docker compose up -d

# Make migrations
docker compose exec api python manage.py makemigrations

# Migrate the database
docker compose exec api python manage.py migrate_schemas --shared

# Collect static files
docker compose exec api python manage.py collectstatic --noinput

# Load default schema
docker compose exec api python manage.py load_default_schema

# Create super user
# docker compose exec api python manage.py createsuperuser
