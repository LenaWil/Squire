"""
Django settings for base project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from time import strftime

from . import util

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY_FILENAME = os.path.join(BASE_DIR, "squire/secret_key.txt")
SECRET_KEY = util.get_secret_key(SECRET_KEY_FILENAME)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_ENV') != 'PRODUCTION'

if os.getenv('SENTRY_DSN'): # pragma: no cover
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
            os.getenv('SENTRY_DSN'),
            integrations=[DjangoIntegration()],
            # Do not send email addresses to Sentry
            send_default_pii=False
    )

# Hosts on which the application will run
ALLOWED_HOSTS = []
if os.getenv('SQUIRE_ALLOWED_HOSTS'): # pragma: no cover
    ALLOWED_HOSTS += os.getenv('SQUIRE_ALLOWED_HOSTS').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core', # Core Module should load first
    'django.contrib.admin',
    # External Libraries
    'bootstrap4',
    'dynamic_preferences', # Global Preferences
    'dynamic_preferences.users.apps.UserPreferencesConfig', # Per-user preferences
    'recurrence',
    'rest_framework',
    # Internal Components
    'achievements',
    'membership_file',
    'inventory',
    'committees',
    'activity_calendar',
    'utils',
    'boardgames',
    'roleplaying',
    'nextcloud_integration',
    'user_interaction.apps.UserInteractionConfig',
    # More External Libraries
    'django_cleanup.apps.CleanupConfig',
    'martor',
    'import_export',
    'pwa',
]


PRE_DEBUG_MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', # Determine Language based on user's Language preference
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

POST_DEBUG_MIDDLEWARE = [
    'membership_file.middleware.MembershipMiddleware',
]

if DEBUG and os.getenv('DJANGO_ENV') != 'TESTING':
    # django-debug-toolbar settings
    INSTALLED_APPS.append('debug_toolbar')
    INTERNAL_IPS = [
        '127.0.0.1',
    ]

    # Should come as early as possible, but after middleware
    #   that changes the response's content
    PRE_DEBUG_MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

# Set Middleware
MIDDLEWARE = PRE_DEBUG_MIDDLEWARE + POST_DEBUG_MIDDLEWARE


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'core.backends.BaseUserBackend',
    'committees.backends.AssociationGroupAuthBackend',
]

ROOT_URLCONF = 'squire.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'squire/templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'dynamic_preferences.processors.global_preferences',
                'membership_file.processor.member_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'squire.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Default primary key field field type to use for models that don't have a field with primary_key=True
#   This changed to BigAutoField in Django 3.2, but migrating to it doesn't work properly
#   for ManyToManyFields that do _not_ have an explicit `through` attribute set.
#   See: https://docs.djangoproject.com/en/3.2/ref/settings/#std-setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/
# https://samulinatri.com/blog/django-translation

LANGUAGE_CODE = 'en-gb'
#LANGUAGE_CODE = 'nl'

LANGUAGES = [
    ('en', 'English'),
    ('nl', 'Dutch'),
]

TIME_ZONE = 'Europe/Amsterdam'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# Log Settings
APPLICATION_LOG_LEVEL = 'INFO'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            # exact format is not important, this is the minimum information
            'format': '%(asctime)s (%(name)-12s) [%(levelname)s] %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'squire': {
            'handlers': ['console'],
            'level': APPLICATION_LOG_LEVEL,
        },
        'core': {
            'handlers': ['console'],
            'level': APPLICATION_LOG_LEVEL,
        },
        'activity_calendar': {
            'handlers': ['console'],
            'level': APPLICATION_LOG_LEVEL,
        },
        'membership_file': {
            'handlers': ['console'],
            'level': APPLICATION_LOG_LEVEL,
        },
        'achievements': {
            'handlers': ['console'],
            'level': APPLICATION_LOG_LEVEL,
        },
    },
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'htdocs', 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'htdocs', 'media')

# Additional places to look for static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'core', 'static_compiled'),
]


# The directory in which the coverage reports should be stored
COVERAGE_REPORT_DIR = os.path.join(BASE_DIR, 'coverage')

# Automatically create a /coverage folder if it does not exist
util.create_coverage_directory(COVERAGE_REPORT_DIR)

####################################################################
# Login Settings

# The URL or named URL pattern where requests are redirected for login
# when using the login_required() decorator.
# Also used to specify the location of the login page
LOGIN_URL = '/login'

# The URL or named URL pattern where requests are redirected after
# login when the LoginView doesn’t get a next GET parameter.
LOGIN_REDIRECT_URL = '/' # Redirect to homepage

# Not a native Django-setting, but used to specify the location of the logout page
LOGOUT_URL = '/logout'

# The URL or named URL pattern where requests are redirected after
# logout if LogoutView doesn’t have a next_page attribute.
LOGOUT_REDIRECT_URL = '/logout/success'

####################################################################
# Martor settings (Markdown Editor)
# https://github.com/agusmakmun/django-markdown-editor

# Global martor settings
MARTOR_ENABLE_CONFIGS = {
    'emoji': 'true',        # to enable/disable emoji icons.
    'imgur': 'true',        # to enable/disable imgur/custom uploader.
    'mention': 'false',     # to enable/disable mention
    'jquery': 'true',       # to include/revoke jquery (require for admin default django)
    'living': 'false',      # to enable/disable live updates in preview
    'spellcheck': 'true',   # to enable/disable spellcheck in form textareas
    'hljs': 'true',         # to enable/disable hljs highlighting in preview
}

# To show the toolbar buttons
MARTOR_TOOLBAR_BUTTONS = [
    'bold', 'italic', 'horizontal', 'heading', 'pre-code',
    'blockquote', 'unordered-list', 'ordered-list',
    'link', 'image-link', 'image-upload', 'emoji',
    #'direct-mention',
    'toggle-maximize', 'help'
]

# Markdown extensions
MARTOR_MARKDOWN_EXTENSIONS = [
    'markdown.extensions.abbr',         # Abbreviations: *[ABBR]
    'markdown.extensions.fenced_code',  # Code blocks: ```CODE```
    # 'markdown.extensions.footnotes',  # Footnotes: [^LABEL]
                                        #   NB: These cause a severe slowdown
    'markdown.extensions.tables',       # Tables
    'markdown.extensions.nl2br',        # New lines as hard breaks (like GitHub)
    'markdown.extensions.sane_lists',   # Prevent mixing (un)ordered lists
    'markdown.extensions.smarty',       # ASCII dashes, quotes and ellipses to their HTML entity equivalents

    # Custom markdown extensions.
    'pymdownx.details',                 # <details> and <summary>: ???+ "SUMMARY TITLE"
    'martor.extensions.urlize',         # Convert urls to links
    'martor.extensions.del_ins',        # ~~strikethrough~~ and ++underscores++
    #'martor.extensions.mention',       # Martor mentions
    'martor.extensions.emoji',          # Martor emoji
    # 'martor.extensions.mdx_video',    # Embed/iframe video (E.g. Youtube, Vimeo, etc.)
    'martor.extensions.escape_html',    # Handle XSS vulnerabilities
]

# Markdown Extensions Configs
MARTOR_MARKDOWN_EXTENSION_CONFIGS = {}

# Enable label in forms
MARTOR_ENABLE_LABEL = True

# Markdown urls
MARTOR_MARKDOWNIFY_URL = '/api/martor/markdownify/'
# MARTOR_SEARCH_USERS_URL = '/martor/search-user/' # for mention

# Markdown Extensions
MARTOR_MARKDOWN_BASE_EMOJI_URL = 'https://github.githubassets.com/images/icons/emoji/'  # default from github
MARTOR_MARKDOWN_BASE_MENTION_URL = ''

# Upload images to local storage
MARTOR_UPLOAD_PATH = os.path.join('images', 'uploads')
MARTOR_UPLOAD_URL = '/api/martor/image_uploader/'

# Maximum Upload Image
# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_IMAGE_UPLOAD_SIZE = 2621440  # 2.5MB

# Valid models for which MarkdownImages can be selected
#   (used internally to handle uploads; Not a Martor setting)
MARKDOWN_IMAGE_MODELS = (
    'activity_calendar.activity', 'activity_calendar.activitymoment',
    'committees.associationgroup',
    'roleplaying.roleplayingsystem'
)

# Maror static overrides
MARTOR_ALTERNATIVE_JS_FILE_THEME = None
MARTOR_ALTERNATIVE_CSS_FILE_THEME = "theming/martor-admin-bootstrap.css" # default None
MARTOR_ALTERNATIVE_JQUERY_JS_FILE = None

####################################################################
# Other Settings
# Non-native Django setting
APPLICATION_NAME = 'Squire'
COMMITTEE_ABBREVIATION = 'UUPS'
COMMITTEE_FULL_NAME = 'UUPS Ultraviolet Programmer Squad'

# The email address that error messages come from, such as those sent to ADMINS and MANAGERS.
SERVER_EMAIL = f'{APPLICATION_NAME} Error <{APPLICATION_NAME.lower()}-error@kotkt.nl>'

# Default email address to use for various automated correspondence from the site manager(s).
DEFAULT_FROM_EMAIL = f'{APPLICATION_NAME} <{APPLICATION_NAME.lower()}-noreply@kotkt.nl>'

# Debug settings
# Also run the following command to imitate an SMTP server locally: python -m smtpd -n -c DebuggingServer localhost:1025
# Emails that are sent will be shown in that terminal
if DEBUG:
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_USE_TLS = False


# Easy way to debug the application at a specific datetime
#   This is obviously an ugly hack and should not be used in production
if DEBUG and False: # pragma: no cover
    from django.utils import timezone
    from datetime import datetime
    timezone.now = lambda: datetime(year=2021, month=9, day=14, hour=21, minute=20, tzinfo=timezone.utc)
    print("=====WARNING=====")
    print("timezone.now was overridden")
    print("It will be " + str(timezone.now()) + " until the end of times!")
    print("You will not escape!")
    print("=================")


# PWA settings
PWA_APP_NAME = 'Squire'
PWA_APP_DESCRIPTION = "The digital home for Knights members."
PWA_APP_THEME_COLOR = '#206141'
PWA_APP_BACKGROUND_COLOR = '#206141'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {
        'src': '/static/images/non_maskable_icon_x512.png',
        'sizes': '512x512'
    },
    {
        'src': '/static/images/non_maskable_icon_x192.png',
        'sizes': '192x192'
    },
    {
        'src': '/static/images/maskable_icon_x512.png',
        'sizes': '512x512',
        'purpose': 'maskable'
    },
    {
        'src': '/static/images/maskable_icon_x192.png',
        'sizes': '192x192',
        'purpose': 'maskable'
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': '/static/images/non_maskable_icon_x512.png',
        'sizes': '512x512'
    },
    {
        'src': '/static/images/non_maskable_icon_x192.png',
        'sizes': '192x192'
    },
    {
        'src': '/static/images/maskable_icon_x512.png',
        'sizes': '512x512',
        'purpose': 'maskable'
    },
    {
        'src': '/static/images/maskable_icon_x192.png',
        'sizes': '192x192',
        'purpose': 'maskable'
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': '/static/images/header_logo.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_SERVICE_WORKER_PATH =  os.path.join(BASE_DIR, 'core', 'static', 'js', 'serviceworker.js')
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'

try:
    from .local_settings import *
except ImportError:
    try:
        util.create_local_settings(
            os.path.join(BASE_DIR, 'squire', 'local_settings.py')
        )
    except FileExistsError:
        pass
