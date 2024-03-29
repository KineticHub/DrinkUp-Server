# Django settings for DrinkUp project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

#os.environ["DJANGO_SETTINGS_MODULE"] = '/opt/bitnami/apps/django/django_projects/DrinkUp/'

ADMINS = (
    ('K. Alnajar', 'kalnajar@gmail.com'),
)

MANAGERS = ADMINS
AUTH_PROFILE_MODULE = 'DrinkUp.VenueOwnerUserProfile'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'drinkup_db',                      # Or path to database file if using sqlite3.
        'USER': 'drinkup_db_user',                      # Not used with sqlite3.
        'PASSWORD': 'Gr@$$h0pper',                  # Not used with sqlite3.
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

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
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '~/apps/django/django_projects/DrinkUp/DrinkUp/static'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

# Facebook related Settings
FACEBOOK_APP_ID = '428379253908650'
FACEBOOK_SECRET_KEY = '22fce7553dbac54a6fa3a67e0c35568f'
FACEBOOK_REDIRECT_URL = 'https://DrinkUp-App.com/facebook/login/success'

# Additional locations of static files
STATICFILES_DIRS = (
    #"/opt/bitnami/apps/django/django_projects/DrinkUp/bootstrap",
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '~/apps/django/django_projects/DrinkUp/DrinkUp/static',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'vp5xc+l#3d)%=i5-v7=1_r@^!9@3g+nd$ofks#-0#^cgf8d#r1'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'DrinkUp.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'DrinkUp.wsgi.application'

# Find templates in the same folder as settings.py.
SETTINGS_PATH = os.path.realpath(os.path.dirname(__file__))

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SETTINGS_PATH, 'templates/'),
    '/templates/',
    'opt/bitnami/apps/django/django_projects/DrinkUp/DrinkUp/templates',
)

#AMAZON BUCKETS
DRINKUP_USER_IMAGES_PROD = 'DrinkUp-Users/'
DRINKUP_USER_IMAGES_DEV = 'DrinkUp-Users-Dev/'

DRINKUP_USER_IMAGES = DRINKUP_USER_IMAGES_DEV if DEBUG else DRINKUP_USER_IMAGES_PROD

AMAZON_IMAGE_BASE_URL = 'https://s3.amazonaws.com/' + DRINKUP_USER_IMAGES

#DJANGO EMAIL VAR
EMAIL_SENDER_PREFIX = 'DrinkUp'
MANDRILL_API_KEY = "VXljMAygdNGr9hlhCzNJZA"
EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"

#DJANGO_EMAIL_SETTINGS
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'developer@letsdrinkup.com'
EMAIL_HOST_PASSWORD = 'LetsDrinkUp'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'developer@letsdrinkup.com'

#DJANGO_SESSION_SETTINGS
SESSION_COOKIE_AGE = 15778500 # 6 months
SESSION_COOKIE_SECURE = True # only send via HTTPS
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_NAME = 'CSRF-TOKEN'

ACCOUNT_ACTIVATION_DAYS = 7

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_NAME = 'CSRF-TOKEN'

GRAPPELLI_ADMIN_TITLE = 'DrinkUp'

SERIALIZATION_MODULES = {
    'json': 'wadofstuff.django.serializers.json'
}

BALANCED_API_KEY_LIVE='d22efde4d52611e2bf68026ba7f8ec28'
BALANCED_API_KEY_TEST='5f3e2ee0a3b211e28fc8026ba7f8ec28'

UA_APP_KEY_DEV = 'eKW8DeUHRBeIUkcKKAbc1g'
UA_APP_SECRET_DEV = 'gV7KroWvRu-pd2QdUETegw'
UA_APP_MASTER_SECRET_DEV = 'BY3UQjEwR9W4bnggTiOafA'

UA_APP_KEY_PROD = 'KqdTDnAMSsmtk2SDyV5YVg'
UA_APP_SECRET_PROD = 'PyGiTKt6S-Cg8d0mHhOwWw'
UA_APP_MASTER_SECRET_PROD = 'X8yvJw9pSVGjahDEOYCJzA'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.flatpages',
    'django_extensions',
    'registration',
    'ApiApp',
	'VenueApp',
	'BarApp',
	'UsersApp',
    'south',
    'grappelli',
    'mathfilters',
    'djrill',
    'timezone_field',
    #'admin_bootstrap',
    #'bootstrap_admin',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
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
