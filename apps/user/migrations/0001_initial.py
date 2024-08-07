# Generated by Django 5.0.7 on 2024-08-06 07:38

import apps.user.models.user_model
import django.contrib.auth.validators
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, error_messages={'unique': 'User with the uid already exists'}, primary_key=True, serialize=False, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()])),
                ('email', apps.user.models.user_model.LowerCaseEmailAddressField(max_length=254, unique=True, verbose_name='email')),
                ('first_name', models.CharField(blank=True, max_length=60, verbose_name='first_name')),
                ('last_name', models.CharField(blank=True, max_length=60, verbose_name='last_name')),
                ('is_staff', models.BooleanField(default=False, verbose_name='is_staff')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='is_deleted')),
                ('deleted_at', models.DateTimeField(default=None, null=True, verbose_name='deleted_at')),
                ('is_verified', models.BooleanField(default=False, verbose_name='is_verified')),
                ('is_active', models.BooleanField(default=False, verbose_name='is_active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated_at')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='TokenVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this code should be treated as active. ', verbose_name='active')),
                ('expiring_time', models.DateTimeField(blank=True, default=None, null=True)),
                ('type', models.CharField(blank=True, choices=[('forget_password', 'forget_password'), ('register', 'register'), ('resend_token', 'resend_token')], default='register', max_length=30, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='token', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'token_verifications',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='profile_images')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user_profile',
                'verbose_name_plural': 'user_profiles',
                'db_table': 'user_profile',
            },
        ),
    ]
