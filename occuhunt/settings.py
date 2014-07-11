# Django settings for occuhunt project.
import os.path
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Sanchit Bareja', 'sanchitbareja@gmail.com'), ('Sidwyn Koh', 'sidwyn@gmail.com'), ('Occuhunt Founders', 'occuhunt@gmail.com'),
)

EMAIL_MASTERS = [email[1] for email in ADMINS]
EMAIL_BACKEND = "mailer.backend.DbBackend"

MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = 'media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = "/media/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = 'static/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
# AWS Storages
AWS_ACCESS_KEY_ID = 'AKIAJMUV3JF5IGAOPF3A'
AWS_SECRET_ACCESS_KEY = 'BwhrrDs7srYGyk9ZHfvn/V1/1dLLx30yg4mFu+Af'
AWS_STORAGE_BUCKET_NAME = 'occuhuntstatic'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = '/static/'

# from S3 import CallingFormat
# AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN

import posixpath
ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, "admin/")

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT,"static"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '#*t!8f*&02lzop+iaa210@8xo34-co3fjq$nuhlm9hd%%b!%-y'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'occuhunt.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'occuhunt.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT,"templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    # third-party apps
    'south',
    'django_extensions',
    'debug_toolbar',
    'tastypie',
    'storages',
    'social.apps.django_app.default',
    'gunicorn',
    'haystack',
    'mailer',
    'provider',
    'provider.oauth2',

    # local apps
    'companies',
    'users',
    'favorites',
    'api',
    'fairs',
    'jobs',
    'resumes',
    'recommendations',
    'hunts',
    'applications',
    'recruiters',
    'notifications',
    'offers',
    'documents'
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# DJANGO DEBUG TOOLBAR
INTERNAL_IPS = ('127.0.0.2',)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

# EMAIL SETTINGS
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'occuhunt@gmail.com'
EMAIL_HOST_PASSWORD = 'downtownberkeleysbsk'
EMAIL_PORT = 587

# Tastypie settings
TASTYPIE_DEFAULT_FORMATS = ['json']
API_LIMIT_PER_PAGE = 20

# Django Social Auth setup
AUTHENTICATION_BACKENDS = (
    'social.backends.linkedin.LinkedinOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = '/login/linkedin/'
LOGIN_REDIRECT_URL = '/events/'
LOGIN_ERROR_URL = '/login-error/'
AUTH_USER_MODEL = 'users.User'
SOCIAL_AUTH_USER_MODEL = AUTH_USER_MODEL
SOCIAL_AUTH_RAISE_EXCEPTIONS = True
# LinkedIn specific config
SOCIAL_AUTH_LINKEDIN_KEY = 'xu79xm7p77of'
SOCIAL_AUTH_LINKEDIN_SECRET = 'UnJhJkwNuUru2m4Y'
SOCIAL_AUTH_LINKEDIN_SCOPE = ['r_basicprofile', 'r_emailaddress', 'r_fullprofile','r_contactinfo','r_network','w_messages']
SOCIAL_AUTH_LINKEDIN_FIELD_SELECTORS = [
    'email-address',
    'headline',
    'industry',
    'location',
    'positions',
    'educations',
    'skills',
]

SOCIAL_AUTH_LINKEDIN_EXTRA_DATA = [('id', 'id'),
                       ('first-name', 'first_name'),
                       ('last-name', 'last_name'),
                       ('email-address', 'email_address'),
                       ('headline', 'headline'),
                       ('industry', 'industry'),
                       ('location', 'location'),
                       ('positions', 'positions'),
                       ('educations', 'educations'),
                       ('skills', 'skills')]

# LINKEDIN_FORCE_PROFILE_LANGUAGE = True
# LINKEDIN_FORCE_PROFILE_LANGUAGE = 'en-US'

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'social.pipeline.partial.save_status_to_session',
    'api.pipeline.create_password',
    'api.pipeline.associate_group',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES = {'default': dj_database_url.config()}

# base root url
BASE_URL = "http://www.occuhunt.com/"

try:
    from occuhunt.settings_local import DATABASES
    from occuhunt.settings_local import HAYSTACK_CONNECTIONS
except Exception:
    # Django-Haystack settings - used for search and indexing
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': os.environ['SEARCHBOX_URL'],
            'INDEX_NAME': 'documents',
            },
        }
    
    }

    pass # there is no local settings file
