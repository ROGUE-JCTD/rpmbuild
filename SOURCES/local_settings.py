# -*- coding: utf-8 -*-

from geoshape.settings import INSTALLED_APPS

SITENAME = 'GeoSHAPE'
SITEURL = 'https://localhost/'
DEBUG = True

ALLOWED_HOSTS = ['localhost']

PROXY_ALLOWED_HOSTS = (
'*',
)

ADMINS = (
)

CLASSIFICATION_BANNER_ENABLED = False
CLASSIFICATION_TEXT = ''
CLASSIFICATION_TEXT_COLOR = ''
CLASSIFICATION_BACKGROUND_COLOR = ''
CLASSIFICATION_LINK = ''

SERVER_EMAIL = 'GeoSHAPE@localhost'
DEFAULT_FROM_EMAIL = 'webmaster@localhost'
REGISTRATION_OPEN = False


DATABASE_ENGINE = 'postgresql_psycopg2'
DATABASE_NAME = 'geoshape'
DATABASE_USER = 'geoshape'
DATABASE_PASSWORD = 'THE_DATABASE_PASSWORD'
DATABASE_HOST = 'localhost'
DATABASE_PORT = '5432'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DATABASE_NAME,
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': DATABASE_PORT,
    },
    'geoshape_imports': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'geoshape_data',
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': DATABASE_PORT,
    }
}

GEOSERVER_URL = SITEURL + 'geoserver/'

# OGC (WMS/WFS/WCS) Server Settings
OGC_SERVER = {
    'default' : {
        'BACKEND' : 'geonode.geoserver',
        'LOCATION' : GEOSERVER_URL,
        'PUBLIC_LOCATION' : GEOSERVER_URL,
        'USER' : 'admin',
        'PASSWORD' : 'geoserver',
        'MAPFISH_PRINT_ENABLED' : True,
        'PRINT_NG_ENABLED' : True,
        'GEONODE_SECURITY_ENABLED' : True,
        'GEOGIG_ENABLED' : True,
        'WMST_ENABLED' : False,
        'DATASTORE': 'geoshape_imports',
        'GEOGIG_DATASTORE_DIR':'/var/lib/geoserver_data/geogig',
    }
}
#  Database datastore connection settings
GEOGIG_DATASTORE_NAME = 'geogig-repo'

UPLOADER = {
    'BACKEND' : 'geonode.importer',
    'OPTIONS' : {
        'TIME_ENABLED' : True,
        'GEOGIG_ENABLED' : True,
    }
}

MEDIA_ROOT = '/var/lib/geonode/uwsgi/uploaded'
STATIC_ROOT = '/var/lib/geonode/uwsgi/static/'

# CSW settings
CATALOGUE = {
    'default': {
        'ENGINE': 'geonode.catalogue.backends.pycsw_local',
        'URL': '%scatalogue/csw' % SITEURL,
    }
}

BROKER_URL = 'amqp://guest@127.0.0.1:5672'
CELERY_ALWAYS_EAGER = False
NOTIFICATION_QUEUE_ALL = not CELERY_ALWAYS_EAGER
NOTIFICATION_LOCK_LOCATION = '/var/lib/geonode/uwsgi'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'geonode',
        },
}

INSTALLED_APPS += (
    'haystack',
)

SLACK_ENABLED = False
SLACK_WEBHOOK_URLS = ['']

# Enable CORS (https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS)
CORS_ENABLED = False
