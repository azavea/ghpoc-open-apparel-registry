"""
Django settings for oar project.

Generated by 'django-admin startproject' using Django 2.0.9.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import requests

from django.core.exceptions import ImproperlyConfigured

from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'secret')

# Set environment
ENVIRONMENT = os.getenv('DJANGO_ENV', 'Development')
VALID_ENVIRONMENTS = ('Production', 'Staging', 'Development')
if ENVIRONMENT not in VALID_ENVIRONMENTS:
    raise ImproperlyConfigured(
        'Invalid ENVIRONMENT provided, must be one of {}'
        .format(VALID_ENVIRONMENTS))

LOGLEVEL = os.getenv('DJANGO_LOG_LEVEL', 'INFO')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (ENVIRONMENT == 'Development')

ALLOWED_HOSTS = [
    'localhost',
    'django',
    '.openapparel.org'
]

if ENVIRONMENT in ['Production', 'Staging']:
    # Within EC2, the Elastic Load Balancer HTTP health check will use the
    # target instance's private IP address for the Host header.
    #
    # The following steps lookup the current instance's private IP address
    # (via the EC2 instance metadata URL) and add it to the Django
    # ALLOWED_HOSTS configuration so that health checks pass.
    #
    # Beginning with version 1.17.0 of the Amazon ECS container agent,
    # tasks that use the awsvpc network mode will have to use the
    # ECS Task Metadata endpoint.

    response = requests.get('http://169.254.170.2/v2/metadata')
    if response.ok:
        response = response.json()

        for container in response['Containers']:
          for network in container['Networks']:
            for addr in network['IPv4Addresses']:
              ALLOWED_HOSTS.append(addr)
    else:
        raise ImproperlyConfigured('Unable to fetch instance metadata')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_gis',
    'rest_auth',
    'allauth',
    'allauth.account',
    'rest_auth.registration',
    'watchman',
    'api',
    'web',
]

# For allauth
SITE_ID = 1

AUTH_USER_MODEL = 'api.User'

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'api.serializers.UserSerializer',
}

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'rollbar.contrib.django_rest_framework.post_exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'spa.middleware.SPAMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddlewareExcluding404',
]

ROOT_URLCONF = 'oar.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'oar.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT')
    }
}


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

# User model
# https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#substituting-a-custom-user-model

AUTH_USER_MODEL = 'api.User'

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Email
# https://docs.djangoproject.com/en/2.0/topics/email

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django_amazon_ses.EmailBackend'

DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@staging.openapparel.org')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_STORAGE = 'spa.storage.SPAStaticFilesStorage'

# Watchman
WATCHMAN_ERROR_CODE = 503
WATCHMAN_CHECKS = (
    'watchman.checks.databases',
)

# Application settings
MAX_UPLOADED_FILE_SIZE_IN_BYTES = 5242880

GOOGLE_GEOCODING_API_KEY = os.getenv('GOOGLE_GEOCODING_API_KEY')
if GOOGLE_GEOCODING_API_KEY is None:
    raise ImproperlyConfigured(
        'Invalid GOOGLE_GEOCODING_API_KEY provided, must be set')

if not DEBUG:
    ROLLBAR = {
        'access_token': os.getenv('ROLLBAR_SERVER_SIDE_ACCESS_TOKEN'),
        'environment': ENVIRONMENT.lower(),
        'root': BASE_DIR,
    }
    import rollbar
    rollbar.init(**ROLLBAR)
