"""
Django settings for lab_attendance_system_backend project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import environ
import logging

log = logging.getLogger(__name__)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# environment variable
# using package: django-environ, doc: https://django-environ.readthedocs.io/en/latest/
# default value is suitable for debugging but not production
env = environ.Env(
    DEBUG=(bool, True),
    SECRET_KEY=(
        str,
        'django-insecure-k3r&2%o=58&q3v&kabgwn&6z3_ftwo!b5rc$7*36ezyx7mfz!)'
    ),
    DATABASE_URL=(
        str,
        'sqlite:///db.sqlite3'
    ),
    GENERAL_LOG_LEVEL=(
        str,
        'INFO'
    ),
    PRIMARY_HOSTNAME=(
        str,
        '127.0.0.1'
    ),
)

environ.Env.read_env(BASE_DIR / '.env')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

if DEBUG:
    log.warning('Enabled DEBUG: True')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')


ALLOWED_HOSTS = [
    env('PRIMARY_HOSTNAME')
]

APPEND_SLASH = False

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dynamic_preferences',
    'rest_framework',
    'knox',
    'django_filters',
    'rest_api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lab_attendance_system_backend.urls'

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

WSGI_APPLICATION = 'lab_attendance_system_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': env.db_url('DATABASE_URL'),
}

# Model used for authentication
# https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-AUTH_USER_MODEL
AUTH_USER_MODEL = 'rest_api.User'

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Singapore'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Logging configurations
# https://docs.djangoproject.com/en/4.1/howto/logging/#logging-how-to
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname}|{asctime}|{module}: {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },

    'handlers': {
        'console': {
            'level': env('GENERAL_LOG_LEVEL'),
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'general_file': {
            'level': env('GENERAL_LOG_LEVEL'),
            'filters': ['require_debug_false'],
            'formatter': 'verbose',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/general.log',
            'maxBytes': 1024*1024*10,  # 10MB
            'backupCount': 10,
        },
        'dbg_file': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'formatter': 'verbose',
            'class': 'logging.FileHandler',
            'filename': 'logs/debug.log',
        },
        # 'mail_admins': {
        #     'level': 'ERROR',
        #     'class': 'django.utils.log.AdminEmailHandler',
        #     'filters': ['to be determined']
        # },
    },

    'loggers': {
        '': {
            'handlers': ['dbg_file', 'general_file', 'console'],
            'level': 'DEBUG',
        },
    },
}

# Django REST Framework config
# https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'knox.auth.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),

    # pagination
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
}

# Customized Config

# the special user id used to refer currently authenticated user
USER_SELF_ID = 'me'
