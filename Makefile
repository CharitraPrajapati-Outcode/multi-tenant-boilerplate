### Makefile --- Makefile for glimpse

# Build docker container
# docker build --no-cache -f Dockerfile -t glimpse .
.PHONY: build
build:
	docker compose build

# Run docker container
.PHONY: run
run:
	docker compose up

# Run docker container in background
.PHONY: run_background
run_background:
	docker compose up -d

# Restart docker container
.PHONY: restart
restart:
	docker compose restart

# Stop docker container
.PHONY: stop
stop:
	docker compose stop

# Remove docker container
.PHONY: remove
remove:
	docker compose down

# Makemigrations using docker compose [RUN: make makemigrations app_name=<app_name>]
.PHONY: makemigrations
makemigrations:
	docker compose exec api python manage.py makemigrations $(app_name)

# Migrate using docker compose [RUN: make migrate app_name=<app_name> migration_name=<migration_name>]
# Example: Make specific migration from start to migration_name | make migrate app_name=users migration_name=0001
# Example: Make specific app_name all migration revert | make migrate app_name=users migration_name=zero
.PHONY: migrate
migrate:
	docker compose exec api python manage.py migrate $(app_name) $(migration_name)

# migrate schema
.PHONY: migrate_schema
schema_name := test
migrate_schema:
	docker compose exec api python manage.py migrate_schemas --schema ${schema_name} ${app_name} ${migration_name}

# Show migrations using docker compose
.PHONY: showmigrations
showmigrations:
	docker compose exec api python manage.py showmigrations

# Enter docker container using docker compose
.PHONY: enter
enter:
	docker compose exec api /bin/sh

# Install pip requirements using docker compose
.PHONY: install_requirements
install_requirements: requirements.txt
	docker compose exec api pip install -r requirements.txt

# Install new pip package using docker compose [RUN: make install_package package=<package_name>]
.PHONY: install_package
install_package:
	docker compose exec api pip install $(package)

# Remove pip package using docker compose [RUN: make remove_package package=<package_name>]
.PHONY: remove_package
remove_package:
	docker compose exec api pip uninstall $(package)

# Update pip version using docker compose
.PHONY: upgrade_pip
upgrade_pip:
	docker compose exec api pip install --upgrade pip


# enter shell using docker compose
.PHONY: enter_shell
enter_shell:
	docker compose exec api python manage.py shell

# Enter PostgreSQL shell
.PHONY: psql
user := postgres
psql:
	docker compose exec db psql -U $(user)
# docker compose exec db psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

# Create new Django app
.PHONY: startapp
startapp:
	docker compose exec api mkdir -p apps/$(app_name) && \
	docker compose exec api python manage.py startapp $(app_name) apps/$(app_name)

# # setup django tenants default schema
.PHONY: load_default_schema
load_default_schema:
	docker compose exec api python manage.py load_default_schema

# # create super user
.PHONY: createsuperuser
createsuperuser:
	docker compose exec api python manage.py createsuperuser

# create schema
.PHONY: create_schema
create_schema:
	docker compose exec api python manage.py create_schema

# remove schema
.PHONY: remove_schema
remove_schema:
	docker compose exec api python manage.py delete_schema

# # run test
.PHONY: test
test := test
test:
	docker compose exec api python manage.py $(test)

# setup database for testing
# Example: make setup_test_database database_name=test_db
.PHONY: run-command
run-command:
	docker compose exec api python manage.py $(command)