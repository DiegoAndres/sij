"""
Django settings for sij project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cz0tkufdt(obpha(1^b#94#nnw_)mq7dl+c5i)9n4cutvizj5*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

# ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
ALLOWED_HOSTS = ['*']


TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__),'templates'),
)

TEMPLATE_LOADERS = (
    # 'django.template.loaders.filesystem.load_template_source',
    # 'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# Application definition

INSTALLED_APPS = (
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sij.apps.causas',
    'sij.apps.home',
    'sij.apps.estadistica',
    'sij.apps.estampado',
    'sorting_bootstrap',
    'bootstrap3',
    'googlecharts',
    # 'debug_toolbar',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


BOOTSTRAP3_DEFAULTS = {
    'css_url': '/media/bootstrap/bootstrap.min.css',
    'theme_url': '/media/bootstrap/bootstrap-theme.min.css',
    'javascript_url': '/media/bootstrap/bootstrap.min.js',
}

# DEBUG_TOOLBAR_PANELS = [
#     'debug_toolbar.panels.versions.VersionsPanel',
#     'debug_toolbar.panels.timer.TimerPanel',
#     'debug_toolbar.panels.settings.SettingsPanel',
#     'debug_toolbar.panels.headers.HeadersPanel',
#     'debug_toolbar.panels.request.RequestPanel',
#     'debug_toolbar.panels.sql.SQLPanel',
#     'debug_toolbar.panels.staticfiles.StaticFilesPanel',
#     'debug_toolbar.panels.templates.TemplatesPanel',
#     'debug_toolbar.panels.cache.CachePanel',
#     'debug_toolbar.panels.signals.SignalsPanel',
#     'debug_toolbar.panels.logging.LoggingPanel',
#     'debug_toolbar.panels.redirects.RedirectsPanel',
# ]


ROOT_URLCONF = 'sij.urls'

WSGI_APPLICATION = 'sij.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'qwerty_sijdev',
        'USER': 'sijdev',
        'PASSWORD': '0303456nanana',
        'HOST':'',
        'PORT':'',
        'OPTIONS': {
           "init_command": "SET storage_engine=INNODB",
        }
    }
}
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

MEDIA_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__),'media/'))
MEDIA_URL = '/media/'
CONTENT_TYPES = ['application/pdf', 'image/jpeg', 'image/jpg']
MAX_UPLOAD_SIZE = 20971520 #20 MB

STATIC_URL = '/static/'

# #email
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'qwerty.ltda@gmail.com'
# EMAIL_HOST_PASSWORD = 'sevenfigureswagger'
# EMAIL_PORT = 587
# DEFAULT_FROM_EMAIL = 'qwerty.ltda@gmail.com'

# if DEBUG == True:
#     EMAIL_USE_TLS = False
#     EMAIL_HOST = 'asdf.qwerty.cl'
#     EMAIL_HOST_USER = ''
#     EMAIL_HOST_PASSWORD = ''
#     EMAIL_PORT = 587
#     DEFAULT_FROM_EMAIL = 'prueba@qwerty.cl'
    
# if DEBUG:
    # EMAIL_HOST = 'localhost'
    # EMAIL_PORT = 1025
    # EMAIL_HOST_USER = ''
    # EMAIL_HOST_PASSWORD = ''
    # EMAIL_USE_TLS = False
    # DEFAULT_FROM_EMAIL = 'testing@sij.cl'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'qwerty.ltda@gmail.com'
EMAIL_HOST_PASSWORD = 'sevenfigureswagger'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = 'qwerty.ltda@gmail.com'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# SERVER_EMAIL = 'qwerty.ltda@gmail.com'