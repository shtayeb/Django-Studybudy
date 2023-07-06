"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import logging
import os
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Initialise environment variables
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

SECRET_KEY = env("SECRET_KEY")
APP_ENV = env("APP_ENV",default="local")
DEBUG = False if env("DEBUG") == "False" else True
DJANGO_SETTINGS_MODULE = env('DJANGO_SETTINGS_MODULE',default='core.settings.local')

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "study-buddy-app.up.railway.app",
    "www.study-buddy-app.up.railway.app",
    "*"
]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CSRF_TRUSTED_ORIGINS = [
    "https://study-buddy-app.up.railway.app",
    "http://study-buddy-app.up.railway.app",
]

# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic', 
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # Installed apps
    "allauth",
    "invitations",
    "rest_framework",
   
    "corsheaders",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.github",
    "django_extensions",
    "easyaudit",
    
    # my apps
    "accounts.apps.AccountsConfig",
    "base.apps.BaseConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
   
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "easyaudit.middleware.easyaudit.EasyAuditMiddleware",
   
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    # {
    #     "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/images/"


AUTH_USER_MODEL = "accounts.User"


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOW_ALL_ORIGINS = True


# EMAIL
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")


# ---------- DJANGO ALL AUTH ------------

ACCOUNT_ADAPTER = "invitations.models.InvitationsAdapter"
INVITATIONS_ACCEPT_INVITE_AFTER_SIGNUP = True

ACCOUNT_FORMS = {
    "signup": "accounts.forms.MyUserCreationForm",
}

# Provider specific settings
SITE_ID = 1
SOCIALACCOUNT_PROVIDERS = {
    "github": {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        "VERIFIED_EMAIL": True,
        "APP": {"client_id": "123", "secret": "456", "key": ""},
    }
}

LOGIN_REDIRECT_URL = "/"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_USERNAME_REQUIRED = True
# USERNAME_FIELD = "email"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'



