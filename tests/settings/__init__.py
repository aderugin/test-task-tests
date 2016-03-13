# -*- coding: utf-8 -*-
"""
    Project settings
"""
import os


#==============================================================================
# Django
#==============================================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_DIR = os.path.dirname(BASE_DIR)

SECRET_KEY = 'bp472bf9y^zrzamcr!5(f@(^@7kjv(l4x_11lmihu5u9$hk5@_'

DEBUG = True

ALLOWED_HOSTS = []

SITE_ID = 1

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)


# Application definition

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'tests.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'tests.wsgi.application'


# Internationalization

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Asia/Yekaterinburg'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'public', 'media')

STATIC_ROOT = os.path.join(PROJECT_DIR, 'public', 'static')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)


# Session

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

SESSION_SAVE_EVERY_REQUEST = True

SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 4

SESSION_COOKIE_DOMAIN = None


# Installed apps

INSTALLED_APPS += (
    'compressor',
    'tests.base'
)


#==============================================================================
# Compress
#==============================================================================

COMPRESS_ENABLED = not DEBUG

COMPRESS_OUTPUT_DIR = 'comporess'


#==============================================================================
# Logging
#==============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PROJECT_DIR, 'debug.log'),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'tests.apps': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'tests.base': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

#==============================================================================
# Settings imports
#==============================================================================

# Production settings
if os.environ.get('ENV') == 'production':
    from .production import *

# Develop settings
elif os.environ.get('ENV') == 'develop':
    from .develop import *

# Staging settings
elif os.environ.get('ENV') == 'staging':
    from .staging import *

# Default choice
else:
    from .develop import *

# Local settings
try:
    from .local import *
except ImportError:
    pass
