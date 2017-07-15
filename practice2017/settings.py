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

INSTALLED_APPS = (
    'crispy_forms',
    'widget_tweaks',
    'tellme',
)


class Base(Configuration):
    DEBUG = False

    config_parser.read(os.path.join(PRACTICE_2017_SYSTEM_PATH, 'practice.master.cfg'))
    DATABASES = get_database(config_parser, DEBUG)
    SECRET_KEY = get_parser_value(config_parser, 'ENVIRONMENT', 'SECRET_KEY')

    ALLOWED_HOSTS = []

    CRISPY_TEMPLATE_PACK = 'bootstrap3'

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

    INSTALLED_APPS1 = INSTALLED_APPS + (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # Web apps
        'itis_manage',
        'itis_data_niffler',
        'dal',
        'dal_select2',
        # datetime here
        'datetimewidget',
    )
    INSTALLED_APPS = INSTALLED_APPS1

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'templates'),
                     os.path.join(BASE_DIR, os.path.join('templates', 'itis_manage')),
                     os.path.join(BASE_DIR, os.path.join('templates', 'itis_data_niffler'))]
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

    # Static files (CSS, JavaScript, Images, Bootstrap3)
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]
    DIRNAME = DIR_NAME
    from datetimewidget.widgets import DateTimeWidget, DateWidget
    dateTimeOptions = {
        'format': 'dd-mm-yyyy HH:ii P',
        'autoclose': True,
        'showMeridian': True
    }
    dateOptions = {
        'format': 'dd-mm-yyyy',
        'autoclose': True,
        'showMeridian': True
    }
    widgets = {
        # NOT Use localization and set a default format
        'datetime': DateTimeWidget(options=dateTimeOptions),
        'date': DateWidget(options=dateOptions)
    }
    TELLME_FEEDBACK_EMAIL = ('timurmardanov97@gmail.com',)


class Master(Base):
    config_parser.read(os.path.join(PRACTICE_2017_SYSTEM_PATH, 'practice.master.cfg'))
    DEBUG = False
    DATABASES = get_database(config_parser, DEBUG)
    ALLOWED_HOSTS = "host.for.deployingdotcom"
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': '/var/tmp/django_cache',
            'TIMEOUT': 60,
            'OPTIONS': {
                'MAX_ENTRIES': 1000
            }
        }
    }
    TELLME_FEEDBACK_EMAIL = ('',)


class Dev(Base):
    config_parser.read(os.path.join(PRACTICE_2017_SYSTEM_PATH, 'practice.dev.cfg'))
    DEBUG = True
    DATABASES = get_database(config_parser, DEBUG)
