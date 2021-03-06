"""
Django settings for tools project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", False)
print(f"Debug: {DEBUG}")

ALLOWED_HOSTS = ['*']
INTERNAL_IPS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'storages',
    'channels',
    'account',
    'home',
    'uploader'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tools.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tools.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'surf_live': {
    },
    'bhop_live': {
    },
    'surf_test': {
    },
    'bhop_test': {
    }
}

surf_db_from_env = dj_database_url.config(env='SURF_DATABASE_URL', conn_max_age=500)
DATABASES['surf_live'].update(surf_db_from_env)

surf_db_from_env = dj_database_url.config(env='BHOP_DATABASE_URL', conn_max_age=500)
DATABASES['bhop_live'].update(surf_db_from_env)

surf_db_from_env = dj_database_url.config(env='SURF_TEST_DATABASE_URL', conn_max_age=500)
DATABASES['surf_test'].update(surf_db_from_env)

surf_db_from_env = dj_database_url.config(env='BHOP_TEST_DATABASE_URL', conn_max_age=500)
DATABASES['bhop_test'].update(surf_db_from_env)


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

AUTH_USER_MODEL = 'account.User'

LOGIN_URL = '/account/login/'

LIVE_MAP_URLS = ['https://files.resurfed.com/maplists/elite.txt', 'https://files.resurfed.com/maplists/bhop.txt']

ASGI_APPLICATION = "tools.routing.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get("REDIS_URL")],
        },
    },
}

CELERY_BROKER_URL = os.environ.get("REDIS_URL")

MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")

if not DEBUG:
    AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_BUCKET")
    AWS_S3_REGION_NAME = os.environ.get("AWS_REGION")
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")

    # Tell django-storages the domain to use to refer to static files.
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'