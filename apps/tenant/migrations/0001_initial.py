# Generated by Django 5.0.7 on 2024-08-06 07:38

import django.contrib.auth.validators
import django.db.models.deletion
import django_tenants.postgresql_backend.base
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, error_messages={'unique': 'Company with the uid already exists'}, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(error_messages={'unique': 'Company name already exists'}, max_length=32, unique=True, verbose_name='name')),
                ('company_tenant', models.CharField(error_messages={'unique': 'Company tenant already exists'}, max_length=16, unique=True, validators=[django.contrib.auth.validators.ASCIIUsernameValidator()], verbose_name='company_tenant')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated_at')),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schema_name', models.CharField(db_index=True, max_length=63, unique=True, validators=[django_tenants.postgresql_backend.base._check_schema_name])),
                ('name', models.CharField(max_length=32, verbose_name='name')),
                ('is_active', models.BooleanField(default=True, verbose_name='is_active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated_at')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(db_index=True, max_length=253, unique=True)),
                ('is_primary', models.BooleanField(db_index=True, default=True)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='domains', to='tenant.tenant')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
