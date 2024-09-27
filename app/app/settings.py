import os

from dotenv import load_dotenv
from pathlib import Path


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent

if os.environ.get('PROD') == "1":
    SECRET_KEY = os.environ.get('DJANGO_SECRET')

    DEBUG = False

    ALLOWED_HOSTS = ['secret1']

    CSRF_COOKIE_SECURE = True
    CSRF_TRUSTED_ORIGIN = ['secret2']
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    SESSION_COOKIE_SECURE = True

    EMAIL_PORT = 'secret3'
    EMAIL_USER_SSL = True
else:
    SECRET_KEY = os.environ.get('DJANGO_SECRET')

    DEBUG = True

    ALLOWED_HOSTS = ['*']

    EMAIL_PORT = '587'
    EMAIL_USE_TLS = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'bugtracker.apps.BugtrackerConfig',
    'api.apps.ApiConfig'
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '1000/day'
    },
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'NUM_PROXIES': 1
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

REDIS_USER = os.environ.get("REDIS_USER")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f'redis://{REDIS_USER}:{REDIS_PASSWORD}@redis/1',
        'TIMEOUT': 60 * 10,
    }
}

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app.middleware.timezone.TimezoneMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'templates/base',
            BASE_DIR / 'templates/base/modals',
            BASE_DIR / 'templates/errors',
            BASE_DIR / 'templates/password',
            BASE_DIR / 'templates/registration',
        ],
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

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "precise": {
            "format": "[{levelname}] [{asctime}] {module} [{message}]",
            "datefmt": "%d-%m-%Y %H:%M:%S",
            "style": "{"
            }
        },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "precise"
            },
        },
    "loggers": {
        "django": {
            "handlers": ["console"]
            },
        },
    }

WSGI_APPLICATION = 'app.wsgi.application'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get('POSTGRES_DB'),
        "USER": os.environ.get('POSTGRES_USER'),
        "PASSWORD": os.environ.get('POSTGRES_PASSWORD'),
        "HOST": os.environ.get('POSTGRES_HOST'),
        "PORT": os.environ.get('POSTGRES_PORT'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
        '.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
        '.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
        '.NumericPasswordValidator',
    },
]

LANGUAGES = [
    ('en', 'English'),
    ('ru', 'Russian'),
]

USE_I18N = True

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

USE_TZ = True
TIME_ZONE = 'UTC'

STATIC_URL = '/static/'
STATIC_ROOT = '/home/user/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
