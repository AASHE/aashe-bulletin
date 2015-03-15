"""
Django settings for aashe_bulletin project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-m7iu+(0mcb_fh0y6#uj0xep+3b+72f@11_i%^&omsg(qzn68r'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = os.environ.get('DEBUG', False)
TEMPLATE_DEBUG = DEBUG

TEMPLATE_DIRS = (
    BASE_DIR + '/aashe_bulletin/templates/',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)

ALLOWED_HOSTS = [""]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # AASHE Apps
    'aashe.aasheauth',
    'django_constant_contact',
    'bulletin',
    'bulletin.tools.plugins',

    # required by bulletin
    'bootstrap3',
    'bootstrap_pagination',
    'django_bootstrap_breadcrumbs',
    'south',
    'mathfilters',

    # good for development
    'django_extensions'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'aashe_bulletin.urls'

WSGI_APPLICATION = 'aashe_bulletin.wsgi.application'

DATABASES = {'default': dj_database_url.config(env='BULLETIN_DATABASE_URL')}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'aashe_bulletin/static/theme'),
                    os.path.join(BASE_DIR, 'aashe_bulletin/static'),)
STATIC_URL = os.environ.get('STATIC_URL', '/static/')
STATIC_ROOT = os.environ.get('STATIC_ROOT',
                             os.path.join(BASE_DIR, STATIC_URL.strip('/')))

MEDIA_URL = os.environ.get('MEDIA_URL', '/media/')
MEDIA_ROOT = os.environ.get('MEDIA_ROOT',
                            os.path.join(BASE_DIR, MEDIA_URL.strip("/")))

AUTHENTICATION_BACKENDS = ('aashe.aasheauth.backends.AASHEBackend',
                           'django.contrib.auth.backends.ModelBackend')
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

# CORS Setup:
CORS_ORIGIN_ALLOW_ALL = True  # @todo - security risk?
CORS_URLS_REGEX = r'^.*/api/.*$'

# Bulletin Settings:
NUM_POSTS_ON_FRONT_PAGE = 10

BULLETIN_CONTENT_TYPE_PLUGINS = (
    'event',
    'job',
    'new resource',
    'opportunity',
    'story',
)

# Constant Contact secrets:
CONSTANT_CONTACT_API_KEY = os.environ['CONSTANT_CONTACT_API_KEY']
CONSTANT_CONTACT_ACCESS_TOKEN = os.environ['CONSTANT_CONTACT_ACCESS_TOKEN']
CONSTANT_CONTACT_FROM_EMAIL = os.environ['CONSTANT_CONTACT_FROM_EMAIL']
CONSTANT_CONTACT_REPLY_TO_EMAIL = os.environ['CONSTANT_CONTACT_REPLY_TO_EMAIL']
CONSTANT_CONTACT_USERNAME = os.environ['CONSTANT_CONTACT_USERNAME']
CONSTANT_CONTACT_PASSWORD = os.environ['CONSTANT_CONTACT_PASSWORD']

MAILCHIMP_API_KEY = os.environ['MAILCHIMP_API_KEY']

# aasheauth
AASHE_DRUPAL_URI = os.environ['AASHE_DRUPAL_URI']
AASHE_DRUPAL_KEY = os.environ['AASHE_DRUPAL_KEY']
AASHE_DRUPAL_KEY_DOMAIN = os.environ['AASHE_DRUPAL_KEY_DOMAIN']
AASHE_DRUPAL_COOKIE_SESSION = os.environ['AASHE_DRUPAL_COOKIE_SESSION']
AASHE_DRUPAL_COOKIE_DOMAIN = os.environ['AASHE_DRUPAL_COOKIE_DOMAIN']
