# ruff: noqa
from .base import *
import os


# import sentry_sdk

# SENTRY_DSN = env("SENTRY_DSN", default="")

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "sqlite": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR.parent / "db.sqlite3",
    },
}

DB = env("DB", default="sqlite")

DATABASES["default"] = DATABASES[DB]


STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",  # with cashing
        # "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage", # No Caching
    },
}



# sentry_sdk.init(
#     dsn=SENTRY_DSN,
#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     traces_sample_rate=1.0,
#     # Set profiles_sample_rate to 1.0 to profile 100%
#     # of sampled transactions.
#     # We recommend adjusting this value in production.
#     profiles_sample_rate=1.0,
# )
