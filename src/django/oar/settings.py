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
from corsheaders.defaults import default_headers

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

BATCH_JOB_QUEUE_NAME = os.getenv('BATCH_JOB_QUEUE_NAME')
if BATCH_JOB_QUEUE_NAME is None and ENVIRONMENT != 'Development':
    raise ImproperlyConfigured(
        'Invalid BATCH_JOB_QUEU_NAME provided, must be set')

BATCH_JOB_DEF_NAME = os.getenv('BATCH_JOB_DEF_NAME')
if BATCH_JOB_DEF_NAME is None and ENVIRONMENT != 'Development':
    raise ImproperlyConfigured(
        'Invalid BATCH_JOB_DEF_NAME provided, must be set')

EXTERNAL_DOMAIN = os.getenv('EXTERNAL_DOMAIN')
if EXTERNAL_DOMAIN is None and ENVIRONMENT != 'Development':
    raise ImproperlyConfigured(
        'Invalid EXTERNAL_DOMAIN provided, must be set')

# A non-empty value of BATCH_MODE signals that we will only be running batch
# processing management commands
BATCH_MODE = os.getenv('BATCH_MODE', '')

LOGLEVEL = os.getenv('DJANGO_LOG_LEVEL', 'INFO')

GIT_COMMIT = os.getenv('GIT_COMMIT', 'UNKNOWN')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (ENVIRONMENT == 'Development')

ALLOWED_HOSTS = [
    '.openapparel.org',
]

if ENVIRONMENT == 'Development':
    ALLOWED_HOSTS.append('localhost')
    ALLOWED_HOSTS.append('django')

if ENVIRONMENT in ['Production', 'Staging'] and BATCH_MODE == '':
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

    # Ensure Django knows to determine whether an inbound request was
    # made over HTTPS by the ALBs HTTP_X_FORWARDED_PROTO header.
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition

INSTALLED_APPS = [
    'corsheaders',
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
    'drf_yasg',
    'rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_auth.registration',
    'watchman',
    'simple_history',
    'waffle',
    'api',
    'web',
    'ecsmanage',
]

# For allauth
SITE_ID = 1
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_ADAPTER = "api.adapters.OARUserAccountAdapter"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''

AUTH_USER_MODEL = 'api.User'

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'api.serializers.UserSerializer',
    'PASSWORD_RESET_SERIALIZER': 'api.serializers.UserPasswordResetSerializer',
    'PASSWORD_RESET_CONFIRM_SERIALIZER': 'api.serializers.UserPasswordResetConfirmSerializer',
}

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'rollbar.contrib.django_rest_framework.post_exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'api.permissions.IsAuthenticatedOrWebClient',
    ),
    'DEFAULT_PAGINATION_CLASS': 'api.pagination.PageAndSizePagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_THROTTLE_CLASSES': [
        'api.throttles.BurstRateThrottle',
        'api.throttles.SustainedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'burst': '100/minute',
        'sustained': '10000/day',
        'data_upload': '30/minute'
    }
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
        },
    },
    'DOC_EXPANSION': 'none',
    'USE_SESSION_AUTH': False,
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Clickjacking protection is turned off to allow iframes:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'spa.middleware.SPAMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddlewareExcluding404',
    'simple_history.middleware.HistoryRequestMiddleware',
    'waffle.middleware.WaffleMiddleware',
    'api.middleware.RequestLogMiddleware',
    'api.middleware.RequestMeterMiddleware',
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

# Use < 3+ default for ID fields
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


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

# Api Limits
API_FREE_REQUEST_LIMIT = 50

# Caching
# https://docs.djangoproject.com/en/3.2/topics/cache/

MEMCACHED_LOCATION = f"{os.getenv('CACHE_HOST')}:{os.getenv('CACHE_PORT')}"
if DEBUG:
    CACHE_BACKEND = 'django.core.cache.backends.memcached.PyLibMCCache'
else:
    CACHE_BACKEND = 'django_elasticache.memcached.ElastiCache'

CACHES = {
    'default': {
        # Use the default in-memory cache when not specifying cache
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'api_throttling': {
        # Use memcached for API throttling
        'BACKEND': CACHE_BACKEND,
        'LOCATION': MEMCACHED_LOCATION
    }
}

# Logging
# https://docs.djangoproject.com/en/2.1/topics/logging/

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Email
# https://docs.djangoproject.com/en/2.0/topics/email

AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', 'eu-west-1')

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django_amazon_ses.EmailBackend'

DEFAULT_FROM_EMAIL = os.getenv(
    'DEFAULT_FROM_EMAIL', 'noreply@oshstaging.openapparel.org')

NOTIFICATION_EMAIL_TO = os.getenv(
    'NOTIFICATION_EMAIL_TO', 'notification@example.com')

# Notifications

NOTIFICATION_WEBHOOK_TIMEOUT = 10

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = ((os.path.join(STATIC_ROOT, "static")),)

STATICFILES_STORAGE = 'spa.storage.SPAStaticFilesStorage'

# Watchman
# https://github.com/mwarkentin/django-watchman

WATCHMAN_ERROR_CODE = 503
WATCHMAN_CHECKS = (
    'watchman.checks.databases',
    'watchman.checks.caches',
    'api.checks.gazetteercache',
)

# django-ecsmanage
# https://github.com/azavea/django-ecsmanage

ECSMANAGE_ENVIRONMENTS = {
    'default': {
        'TASK_DEFINITION_NAME': 'OpenSupplyHubStagingAppCLI',
        'CONTAINER_NAME': 'django',
        'CLUSTER_NAME': 'ecsOpenSupplyHubStagingCluster',
        'LAUNCH_TYPE': 'FARGATE',
        'PLATFORM_VERSION': '1.4.0',
        'SECURITY_GROUP_TAGS': {
            'Name': 'sgAppEcsService',
            'Environment': 'Staging',
            'Project': 'OpenSupplyHub'
        },
        'SUBNET_TAGS': {
            'Name': 'PrivateSubnet',
            'Environment': 'Staging',
            'Project': 'OpenSupplyHub'
        },
        'AWS_REGION': 'eu-west-1',
    },
    'production': {
        'TASK_DEFINITION_NAME': 'OpenSupplyHubProductionAppCLI',
        'CONTAINER_NAME': 'django',
        'CLUSTER_NAME': 'ecsOpenSupplyHubProductionCluster',
        'LAUNCH_TYPE': 'FARGATE',
        'PLATFORM_VERSION': '1.4.0',
        'SECURITY_GROUP_TAGS': {
            'Name': 'sgAppEcsService',
            'Environment': 'Production',
            'Project': 'OpenSupplyHub'
        },
        'SUBNET_TAGS': {
            'Name': 'PrivateSubnet',
            'Environment': 'Production',
            'Project': 'OpenSupplyHub'
        },
        'AWS_REGION': 'eu-west-1',
    }
}

# Application settings
MAX_UPLOADED_FILE_SIZE_IN_BYTES = 5242880
TILE_CACHE_MAX_AGE_IN_SECONDS = 60 * 60 * 24 * 365 # 1 year. Also in deployment/terraform/cdn.tf  # NOQA

GOOGLE_SERVER_SIDE_API_KEY = os.getenv('GOOGLE_SERVER_SIDE_API_KEY')
if GOOGLE_SERVER_SIDE_API_KEY is None:
    raise ImproperlyConfigured(
        'Invalid GOOGLE_SERVER_SIDE_API_KEY provided, must be set')

if not DEBUG:
    ROLLBAR = {
        'access_token': os.getenv('ROLLBAR_SERVER_SIDE_ACCESS_TOKEN'),
        'environment': ENVIRONMENT.lower(),
        'root': BASE_DIR,
        'suppress_reinit_warning': True,
    }
    import rollbar
    rollbar.init(**ROLLBAR)

OAR_CLIENT_KEY = os.getenv('OAR_CLIENT_KEY')

if OAR_CLIENT_KEY is None:
    raise ImproperlyConfigured(
        'Invalid OAR_CLIENT_KEY provided, must be set')

# Mailchimp settings
MAILCHIMP_API_KEY = os.getenv('MAILCHIMP_API_KEY')
MAILCHIMP_LIST_ID = os.getenv('MAILCHIMP_LIST_ID')

# CORS
# Regex defining which endpoints enable CORS
CORS_URLS_REGEX = r"^/api/info/.*$"
# allows X-OAR-Client-Key to be sent as a header on CORS requests
CORS_ALLOW_HEADERS = list(default_headers) + [
    'X-OAR-Client-Key',
]
# methods that can be used at CORS-enabled endpoints
CORS_ALLOW_METHODS = [
    "GET",
    "OPTIONS",
]
# origins that are authorized to make cross-site HTTP
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://\w+\.openapparel\.org$",
    r"^https://oar\.niceandserious\.com$",
    r"^http://localhost",
    r"http://127.0.0.1",
]
CORS_REPLACE_HTTPS_REFERER = True

# django-storages
# Reference # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html

# To test S3 in development, change this conditional to be True and make sure
# the following are set in the .env file
#   AWS_S3_ACCESS_KEY_ID
#   AWS_S3_SECRET_ACCESS_KEY
#   AWS_STORAGE_BUCKET_NAME
if not DEBUG:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
if AWS_STORAGE_BUCKET_NAME is None and not DEBUG:
    raise ImproperlyConfigured(
        'Invalid AWS_STORAGE_BUCKET_NAME provided, must be set in the environment'
    )
