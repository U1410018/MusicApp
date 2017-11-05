"""
Django settings for Capstone project.

Generated by 'django-admin startproject' using Django 1.11.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*jt$f(591p8*2jobiv4jbcae%00!t=j8_x2eoi2y4nql%1+q)r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # external packages
    'rest_framework',
    'rest_framework.authtoken',
    'pafy',
    'youtube_dl',
    'easy_thumbnails',

    # apps
    'charts',
    'authentication',
    'music',

    'recommends',
    'recommends.storages.djangoorm',
    'django.contrib.sites'

]

SITE_ID = 1

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'PAGE_SIZE': 10
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Capstone.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'Capstone.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

PASSWORD_MINIMUM_LENGTH = 5

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': PASSWORD_MINIMUM_LENGTH,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR,  'static')

STATICFILES_DIRS = [
    'assets',
]

TEMPLATE_DIRS = os.path.join(BASE_DIR,  'templates'),

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MP3_STORAGE = os.path.join(MEDIA_ROOT, 'music')

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'authentication.authentication.EmailAuthBackend',
    # 'tokenapi.backends.TokenBackend',
)

AUTH_USER_MODEL = 'authentication.Profile'

FORMAT_MODULE_PATH = [
    'authentication.formats',
]

LOGIN_REDIRECT_URL = 'index'
LOGIN_URL = 'login'

GEOIP_PATH = os.path.join(BASE_DIR, 'geoip')

DEFAULT_FROM_EMAIL = 'inhaice@gmail.com'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filters': ['require_debug_false'],
            'filename': 'log/error.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

from elasticsearch import Elasticsearch, RequestsHttpConnection
ES_CLIENT = Elasticsearch(
    ['http://127.0.0.1:9200/'],
    connection_class=RequestsHttpConnection
)
ES_AUTOREFRESH = True

RECOMMENDS_TASK_CRONTAB = {'minute': '*/5'}
RECOMMENDS_STORAGE_COMMIT_THRESHOLD = 3

THUMBNAIL_BASEDIR = 'thumbs'
THUMBNAIL_CACHE_DIMENSIONS = True
THUMBNAIL_CHECK_CACHE_MISS = True
THUMBNAIL_DEBUG = True
THUMBNAIL_QUALITY = 95

THUMBNAIL_ALIASES = {
    '': {
        'avatar': {'size': (50, 50), 'crop': True, 'subsampling': 1},
        'new_songs_index': {'size': (161, 161), 'crop': True, 'subsampling': 1},
        'top_albums_index': {'size': (40, 40), 'crop': True, 'subsampling': 1},
        'discover_index': {'size': (188, 281), 'crop': True, 'subsampling': 1},
        'genres': {'size': (154, 154), 'crop': True, 'subsampling': 1},
        'album_cover': {'size': (720, 360), 'crop': True, 'subsampling': 1},
        'playlist_cover': {'size': (800, 400), 'crop': True, 'subsampling': 1},
        'other_playlists_cover': {'size': (486, 243), 'crop': True, 'subsampling': 1},
    },
}
