import sys
from decouple import config


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django_tenants.postgresql_backend',
            'NAME': config('DB_NAME', default="postgres"),
            'USER': config('DB_USER', default="postgres"),
            'PASSWORD': config('DB_PASSWORD', default="password"),
            'HOST': config('DB_HOST', default="localhost"),
            'PORT': config('DB_PORT', default=5432),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django_tenants.postgresql_backend',
            'NAME': config('DB_NAME', default="postgres"),
            'USER': config('DB_USER', default="postgres"),
            'PASSWORD': config('DB_PASSWORD', default="password"),
            'HOST': config('DB_HOST', default="localhost"),
            'PORT': config('DB_PORT', default=5432),
            'OPTIONS': {
                'options': '-c search_path=%s' % config('DB_SCHEMA', default='public')
            }
        }
    }

DATABASE_ROUTERS = ('django_tenants.routers.TenantSyncRouter',)