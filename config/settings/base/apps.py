# Application definition

SHARED_APPS = [
    "django_tenants",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "corsheaders",
    "django_filters",
    "rest_framework",
    "drf_yasg",
    "compressor",

    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "storages",

    "apps.user",
    "apps.core",
    "apps.tenant",
]

TENANT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    
    "corsheaders",

    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "storages",

    "apps.user",
    "apps.core",
]

INSTALLED_APPS = SHARED_APPS + [app for app in TENANT_APPS if app not in SHARED_APPS]