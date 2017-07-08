"""
Django settings for practice2017 project.

Generated by 'django-admin startproject' using Django 1.8.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

import os
import sys
from practice2017.set_lib import get_parser_value, get_database
from configurations import Configuration

try:
    import configparser
except:
    from six.moves import configparser

config_parser = configparser.ConfigParser()
PRACTICE_2017_SYSTEM_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_NAME = os.path.dirname(__file__)

class Base(Configuration):
    DEBUG = False

    config_parser.read(os.path.join(PRACTICE_2017_SYSTEM_PATH, 'practice.master.cfg'))
    DATABASES = get_database(config_parser, DEBUG)
    SECRET_KEY = get_parser_value(config_parser, 'ENVIRONMENT', 'SECRET_KEY')

    ALLOWED_HOSTS = []

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'itis_manage',
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

    ROOT_URLCONF = 'practice2017.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'templates')]
            ,
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

    WSGI_APPLICATION = 'practice2017.wsgi.application'

    # DATABASE configure

    LANGUAGE_CODE = 'ru-RU'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "static"),
        '/static/',
    )
    DIRNAME = DIR_NAME
    STATIC_ROOT = os.path.join(DIRNAME, 'static')


class Dev(Base):
    config_parser.read(os.path.join(PRACTICE_2017_SYSTEM_PATH, 'practice.dev.cfg'))
    DEBUG = True
    DATABASES = get_database(config_parser, DEBUG)