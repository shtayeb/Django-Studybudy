# ruff: noqa
from .base import *
import structlog

LOCAL_INSTALLED_APPS = [
    "nplusone.ext.django",
    "debug_toolbar",
]

INSTALLED_APPS = INSTALLED_APPS + LOCAL_INSTALLED_APPS


LOCAL_MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "nplusone.ext.django.NPlusOneMiddleware",
]

MIDDLEWARE = MIDDLEWARE + LOCAL_MIDDLEWARE

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "sqlite": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR.parent / "db.sqlite3",
    },
    "postgresql": {
        # "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME", default="test"),
        "USER": env("DB_USER", default="root"),
        "PASSWORD": env("DB_PASSWORD", default=""),
        "HOST": env("DB_HOST", default="localhost"),
        "PORT": env("DB_PORT", default="3306"),
    },
}

DB = env("DB", default="sqlite")

DATABASES["default"] = DATABASES[DB]

INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]


STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        # "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage", # with cashing
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",  # No Caching
    },
}

#
NPLUSONE_LOGGER = structlog.get_logger("nplusone")
NPLUSONE_LOG_LEVEL = logging.WARN

DJANGO_VITE_PLUGIN = {
    "BUILD_DIR": "staticfiles/build",
    "BUILD_URL_PREFIX": "/" + STATIC_URL + "build",
    "DEV_MODE": True,
    "SERVER": {"HOST": "0.0.0.0"},
}


structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)



LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
        },
        "plain_console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(),
        },
        "key_value": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.KeyValueRenderer(key_order=["timestamp", "level", "event", "logger"]),
        },
    },
    "handlers": {
        # Important notes regarding handlers.
        #
        # 1. Make sure you use handlers adapted for your project.
        # These handlers configurations are only examples for this library.
        # See python's logging.handlers: https://docs.python.org/3/library/logging.handlers.html
        #
        # 2. You might also want to use different logging configurations depending of the environment.
        # Different files (local.py, tests.py, production.py, ci.py, etc.) or only conditions.
        # See https://docs.djangoproject.com/en/dev/topics/settings/#designating-the-settings
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "plain_console",
        },
        "json_file": {
            "class": "logging.handlers.WatchedFileHandler",
            "filename": os.path.join(BASE_DIR.parent, "logs/json.log"),
            "formatter": "json_formatter",
        },
        "flat_line_file": {
            "class": "logging.handlers.WatchedFileHandler",
            "filename": os.path.join(BASE_DIR.parent, "logs/flat_line.log"),
            "formatter": "key_value",
        },
    },
    "loggers": {
        "django_structlog": {
            "handlers": ["console", "flat_line_file", "json_file"],
            "level": "ERROR",
        },
    },
}
