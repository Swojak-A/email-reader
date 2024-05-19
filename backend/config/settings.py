from enum import Enum
from pathlib import Path

from django.utils.translation import gettext_lazy as _

import sentry_sdk
from celery.schedules import crontab
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from utils import get_env


# ENVIRONMENT MAP
class ENVIRONMENTS(Enum):
    BUILD = "build"
    LOCAL = "local"
    CI = "ci"
    DEVELOP = "develop"
    STAGE = "stage"
    PRODUCTION = "production"


def get_environment_setting():
    env_setting = get_env("ENVIRONMENT")
    try:
        return ENVIRONMENTS(env_setting)
    except ValueError:
        allowed_values = [e.value for e in ENVIRONMENTS]
        raise ValueError(
            f"Invalid ENVIRONMENT value: {env_setting}."
            f"Allowed values are {allowed_values}"
        ) from None


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_env("DEBUG", expected_type=bool)
ALLOWED_HOSTS = get_env("ALLOWED_HOSTS", expected_type=list)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

VERSION = get_env("VERSION")

SITE_ID = 1
DEFAULT_SITE_ID = 1

AUTH_USER_MODEL = "users.User"

ENVIRONMENT = get_environment_setting().value

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.redirects",
    "django.contrib.sitemaps",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_celery_results",
    "django_extensions",
    "kazoo_locks",
    "rest_framework",
    "scheduler",
    "utils",
    "modules.healthchecks",
    "modules.users",
    "modules.email_reader",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            "templates",
        ],
        # 'APP_DIRS': True,
        "OPTIONS": {
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": get_env("DATABASE_NAME"),
        "USER": get_env("DATABASE_USER"),
        "PASSWORD": get_env("DATABASE_PASSWORD"),
        "HOST": get_env("DATABASE_HOST"),
        "PORT": get_env("DATABASE_PORT"),
        "CONN_MAX_AGE": 600,
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # NOQA
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en"

LANGUAGES = (
    ("en", _("English")),
    ("pl", _("Polish")),
)

LOCALE_PATHS = [
    "locale",
]

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = False

USE_TZ = True

STATIC_URL = "/static/" + VERSION + "/"

STATIC_ROOT = BASE_DIR / "collected_static"

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

STATICFILES_DIRS = (BASE_DIR / "static",)

SECURE_HSTS_SECONDS = 2592000
SESSION_COOKIE_AGE = 24 * 60 * 60 * 7

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

REDIS_HOST = get_env("REDIS_HOST")
REDIS_PORT = get_env("REDIS_PORT")

# CACHE
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": [f"redis://{REDIS_HOST}:{REDIS_PORT}/10"],
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PICKLE_VERSION": -1,
        },
    },
}

# DJANGO REST FRAMEWORK

REST_FRAMEWORK = {
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S.%fZ",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PARSER_CLASSES": ("rest_framework.parsers.JSONParser",),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# DRF SPECTACULAR

SPECTACULAR_SETTINGS = {
    "TITLE": "email-reader",
    "DESCRIPTION": "Api documentation",
    "VERSION": "0.0.1",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
}

SENTRY_ENABLED = get_env("SENTRY_ENABLED", expected_type=bool)

SENTRY_TRACES_SAMPLE_RATE = get_env("SENTRY_TRACES_SAMPLE_RATE", float)

SENTRY_PROFILES_SAMPLE_RATE = get_env("SENTRY_PROFILES_SAMPLE_RATE", float)

if SENTRY_ENABLED:
    sentry_sdk.init(
        dsn=get_env("SENTRY_DSN"),
        release=get_env("VERSION"),
        environment=ENVIRONMENT,
        attach_stacktrace=True,
        max_request_body_size="always",
        max_value_length=4096,
        integrations=[
            DjangoIntegration(),
            CeleryIntegration(),
            RedisIntegration(),
        ],
        traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE,
        profiles_sample_rate=SENTRY_PROFILES_SAMPLE_RATE,
    )

# CELERY TASK
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_BEAT_SCHEDULE = {
    "scheduler.tasks.celerybeat_healthcheck": {
        "task": "scheduler.tasks.celerybeat_healthcheck",
        "schedule": crontab(minute="*/1"),
    },
}

CELERY_BROKER_URL = get_env("CELERY_BROKER")
CELERY_RESULT_BACKEND = "django-db"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_DEFAULT_QUEUE = "misc"
CELERY_TASK_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
CELERY_WORKER_HIJACK_ROOT_LOGGER = False

APPEND_SLASH = True

ZOOKEEPER_APP_NAMESPACE = get_env("ZOOKEEPER_APP_NAMESPACE")
ZOOKEEPER_HOSTS = get_env("ZOOKEEPER_HOSTS", expected_type=list)

UWSGI_PROCESS = get_env("UWSGI_PROCESS")

LOGSTASH_ENABLED = get_env("LOGSTASH_ENABLED", expected_type=bool)

LOGGING_HANDLERS = ["console"] + (["logstash"] if LOGSTASH_ENABLED else [])

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",  # NOQA: E501
        },
        "logstash": {
            "()": "logstash_async.formatter.DjangoLogstashFormatter",
            "message_type": "python-logstash",
            "fqdn": True,
            "tags": [get_env("LOGSTASH_TAG")],
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "logstash": {
            "level": "INFO",
            "class": "logstash_async.handler.AsynchronousLogstashHandler",
            "transport": "logstash_async.transport.UdpTransport",
            "port": 5000,
            "host": get_env("LOGSTASH_HOST"),
            "version": 1,
            "database_path": None,
            "formatter": "logstash",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": LOGGING_HANDLERS,
    },
    "loggers": {
        "django": {
            "handlers": LOGGING_HANDLERS,
            "propagate": False,
        },
        "django.db.backends": {
            "level": "ERROR",
            "handlers": LOGGING_HANDLERS,
            "propagate": False,
        },
        "celery": {
            "level": "WARNING",
            "handlers": LOGGING_HANDLERS,
            "propagate": True,
        },
    },
}

# EMAIL READER CONFIG

EMAIL_READER_HOST = get_env("EMAIL_READER_HOST")
EMAIL_READER_USERNAME = get_env("EMAIL_READER_USERNAME")
EMAIL_READER_PASSWORD = get_env("EMAIL_READER_PASSWORD")
