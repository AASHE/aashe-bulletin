"""
Django settings for aashe_bulletin project.
"""
import os
import certifi
from urlparse import urlparse

import dj_database_url
from PIL import ImageFile
from django.contrib.messages import constants as message_constants

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", None)
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", None)
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", None)

AWS_QUERYSTRING_AUTH = False  # Prefer unsigned S3 URLs.

# User uploaded media
DEFAULT_FILE_STORAGE = "s3_folder_storage.s3.DefaultStorage"
DEFAULT_S3_PATH = os.environ.get("DEFAULT_S3_PATH", "uploads")
MEDIA_ROOT = "/%s/" % DEFAULT_S3_PATH
MEDIA_URL = "//s3.amazonaws.com/%s/%s/" % (AWS_STORAGE_BUCKET_NAME, DEFAULT_S3_PATH)

# Static files, served with whitenoise
STATIC_ROOT = "staticfiles"
STATICFILES_STORAGE = "whitenoise.django.GzipManifestStaticFilesStorage"
STATIC_URL = "/static/"

# CDN Settings
CDN_STATIC_HOST = os.environ.get("CDN_STATIC_HOST", None)
if CDN_STATIC_HOST:
    STATIC_URL = "//%s%s" % (CDN_STATIC_HOST, STATIC_URL)

CDN_MEDIA_HOST = os.environ.get("CDN_MEDIA_HOST", None)
if CDN_MEDIA_HOST:
    MEDIA_URL = "//%s/%s/" % (CDN_MEDIA_HOST, DEFAULT_S3_PATH)
    AWS_S3_CUSTOM_DOMAIN = CDN_MEDIA_HOST

ADMIN_MEDIA_PREFIX = STATIC_URL + "admin/"

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = os.environ.get("DEBUG", False)
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": (BASE_DIR + "/aashe_bulletin/templates/",),
        "APP_DIRS": True,
        "OPTIONS": {
            "builtins": ["overextends.templatetags.overextends_tags"],
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.core.context_processors.debug",
                "django.core.context_processors.i18n",
                "django.core.context_processors.media",
                "django.core.context_processors.static",
                "django.core.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "django.core.context_processors.request",
            ],
            "debug": DEBUG,
        },
    }
]

ALLOWED_HOSTS = [".aashe.org"]

ADMINS = (
    ("Rogelio ZunigaRubio", "rogelio@aashe.org"),
    ("Crystal", "crystal.simmons@aashe.org"),
)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.flatpages",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "corsheaders",
    "haystack",
    "aashe_bulletin",  # so aashe_bulletin/management/commands are available
    # AASHE Apps
    "bulletin",
    "bulletin.tools.issue_editor",
    "bulletin.tools.plugins",
    "django_constant_contact",
    # required by our email templates
    "mathfilters",
    "sorl.thumbnail",
    "aashe_bulletin.newsletter",
    # required by bulletin
    "bootstrap3",
    "bootstrap_pagination",
    "datetimewidget",
    "rest_framework",
    # misc 3rd party apps
    "overextends",
    # good for development and debugging
    "django_extensions",
    "template_repl",
]

MIDDLEWARE_CLASSES = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "htmlmin.middleware.HtmlMinifyMiddleware",
    "htmlmin.middleware.MarkRequestMiddleware",
)

ROOT_URLCONF = "aashe_bulletin.urls"

WSGI_APPLICATION = "aashe_bulletin.wsgi.application"

# Assumes DATABASE_URL is set in the env
DATABASES = {"default": dj_database_url.config()}

SITE_ID = 1

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/New_York"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# AASHE's Media Settings
# if not DEBUG:
#     INSTALLED_APPS += ("s3_folder_storage",)
#     STATICFILES_DIRS = (os.path.join(os.path.dirname(__file__), "static"),)

# AASHE's Logging Settings
#    INSTALLED_APPS += ("raven.contrib.django.raven_compat",)

# HEROKU
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# Allow all host headers
ALLOWED_HOSTS = ["*"]

AUTHENTICATION_BACKENDS = (
    # "django_membersuite_auth.backends.MemberSuiteBackend",
    "django.contrib.auth.backends.ModelBackend",
)
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"

# CORS Setup:
CORS_ORIGIN_ALLOW_ALL = False
CORS_URLS_REGEX = r"^.*/api/.*$"
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    "localhost:8000",
    "127.0.0.1:8000",
)

# Bulletin Settings:
NUM_POSTS_ON_FRONT_PAGE = 50
NUM_ADS_ON_ADS_LIST = 30

BULLETIN_CONTENT_TYPE_PLUGINS = (
    "event",
    "job",
    "newresource",
    "opportunity",
    "story",
)

# Constant Contact secrets:
CONSTANT_CONTACT_API_KEY = os.environ["CONSTANT_CONTACT_API_KEY"]
CONSTANT_CONTACT_ACCESS_TOKEN = os.environ["CONSTANT_CONTACT_ACCESS_TOKEN"]
CONSTANT_CONTACT_FROM_EMAIL = os.environ["CONSTANT_CONTACT_FROM_EMAIL"]
CONSTANT_CONTACT_REPLY_TO_EMAIL = os.environ["CONSTANT_CONTACT_REPLY_TO_EMAIL"]
CONSTANT_CONTACT_USERNAME = os.environ["CONSTANT_CONTACT_USERNAME"]
CONSTANT_CONTACT_PASSWORD = os.environ["CONSTANT_CONTACT_PASSWORD"]

# aasheauth
MS_ACCESS_KEY = os.environ["MS_ACCESS_KEY"]
MS_SECRET_KEY = os.environ["MS_SECRET_KEY"]
MS_ASSOCIATION_ID = os.environ["MS_ASSOCIATION_ID"]

SCREEN_IMAGE_UPLOADS = True
SCREEN_IMAGE_LICENSE_TEXT = """
By checking this box, you are granting AASHE an irrevocable,
royalty-free, nonexclusive, and perpetual license to use the submitted
file(s) in publications, newsletters, resources or promotional
materials, and you are hereby representing and warranting that you own
all the rights to the submitted file(s), or have obtained all
necessary licenses and/or permissions to use the submitted file(s),
and that AASHE's use of such file(s) will not infringe the rights of
any third party, including but not limited to intellectual property
rights, or any other rights protected by law (such as the right to
privacy or right of publicity).
"""

# MAX_STORY_TITLE_LENGTH = 90
MAX_STORY_BLURB_LENGTH = 800
MAX_OPPORTUNITY_BLURB_LENGTH = 1100
MAX_NEW_RESOURCE_BLURB_LENGTH = 1100

MESSAGE_TAGS = {
    message_constants.DEBUG: "alert fade in alert-debug",
    message_constants.INFO: "alert fade in alert-info",
    message_constants.SUCCESS: "alert fade in alert-success",
    message_constants.WARNING: "alert fade in alert-warning",
    message_constants.ERROR: "alert fade in alert-error",
}

# Define a css class for required fields so we can mark them.
BOOTSTRAP3 = {"required_css_class": "required-input"}

# Searchbox backend for Haystack
es = urlparse(os.environ.get("SEARCHBOX_URL") or "http://127.0.0.1:9200/")
port = es.port or 80
HAYSTACK_ENGINE = os.environ.get(
    "HAYSTACK_ENGINE",
    "haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine",
)

HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": HAYSTACK_ENGINE,
        "URL": es.scheme + "://" + es.hostname + ":" + str(port),
        "INDEX_NAME": "documents",
        "TIMEOUT": 60 * 5,
    },
}

if es.username:
    HAYSTACK_CONNECTIONS["default"]["KWARGS"] = {
        "http_auth": es.username + ":" + es.password
    }

# HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
def is_member(user):
    return True
    # try:
    #     membersuiteuser = user.membersuiteportaluser
    # except AttributeError:
    #     return False
    # return membersuiteuser.is_member


SEARCH_LOGIN_REQUIRED = False
SEARCH_USER_PASSES_TEST = is_member
SEARCH_USER_FAILS_TEST_URL = "/search-permission-denied/"

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ),
    "DEFAULT_THROTTLE_RATES": {"anon": "100/minute", "user": "100/minute"},
}

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", None)
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", None)
AWS_BUCKET_NAME = os.environ.get("AWS_BUCKET_NAME", None)
AWS_HEADERS = {
    "Expires": "Thu, 1 Jan 2026 20:00:00 GMT",
    "Cache-Control": "max-age:311040000",
}
AWS_QUERYSTRING_AUTH = False

# Because https://github.com/python-pillow/Pillow/issues/1529:
ImageFile.MAXBLOCK = 1024 * 1024
# Because https://github.com/jazzband/sorl-thumbnail/issues/564:
THUMBNAIL_PRESERVE_FORMAT = True
HTML_MINIFY = False
# django debug toolbar
DEBUG_TOOLBAR = os.environ.get("DEBUG", False)
if DEBUG_TOOLBAR:
    INTERNAL_IPS = [
        "127.0.0.1",
    ]
    INSTALLED_APPS.append("debug_toolbar")
    DEBUG_TOOLBAR_CONFIG = {
        "INTERCEPT_REDIRECTS": False,
    }
    DEBUG_TOOLBAR_PATCH_SETTINGS = False
    DEBUG_TOOLBAR_PANELS = [
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.logging.LoggingPanel",
    ]
