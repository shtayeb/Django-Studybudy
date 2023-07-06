from .base import *

LOCAL_INSTALLED_APPS = [
    'nplusone.ext.django',
    "debug_toolbar",
]

INSTALLED_APPS = INSTALLED_APPS + LOCAL_INSTALLED_APPS


LOCAL_MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'nplusone.ext.django.NPlusOneMiddleware',
]

MIDDLEWARE = MIDDLEWARE + LOCAL_MIDDLEWARE

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

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
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage", # No Caching
    },
}

#
NPLUSONE_LOGGER = logging.getLogger('nplusone')
NPLUSONE_LOG_LEVEL = logging.WARN