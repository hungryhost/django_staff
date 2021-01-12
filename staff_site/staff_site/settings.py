"""
Django settings for rentAccess project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
import environ
from pathlib import Path
from datetime import timedelta
# Build paths inside the project like this: BASE_DIR / 'subdir'.
from celery.schedules import crontab
from kombu import Exchange, Queue

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


# SECURITY WARNING: don't run with debug turned on in production!
env = environ.Env(
	DEBUG=(bool, False)
)
environ.Env.read_env()
DEBUG = env('DEBUG')
SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True

# Application definition

SETTINGS_PATH = os.path.normpath(os.path.dirname(__file__))
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'properties',
	'userAccount',
	'corsheaders',
	'common',
	'register',
	'keys',
	'schedule',
	'locks',
	'checkAccess',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'corsheaders.middleware.CorsMiddleware',

]

ROOT_URLCONF = 'staff_site.urls'

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

WSGI_APPLICATION = 'staff_site.wsgi.application'

TEMPLATE_DIRS = (
	os.path.join(SETTINGS_PATH, 'templates'),
)

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': 'rentdbtest',
		"USER": os.environ.get("DB_USER"),
		"PASSWORD": os.environ.get("DB_PASSWORD"),
		"HOST": os.environ.get("DB_HOST", "localhost"),
		"PORT": os.environ.get("DB_PORT", "5432"),
		'OPTIONS': {
			'options': '-c search_path=public'
		},
	}
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Media root and url definitions
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Static root and file definitions
STATICFILES_DIRS = [
	os.path.join(BASE_DIR, "static"),
]
STATIC_URL = '/static/'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = '/static/'

# when DEBUG == True DRF will render errors as html pages


# CELERY CONFIG
if not DEBUG:
	CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
	EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Moscow'
# default_exchange = Exchange('default', type='direct')
# priority_exchange = Exchange('priority_queue', type='direct')

# CELERY_QUEUES = (
#    Queue('default', default_exchange, routing_key='default', consumer_arguments={'x-priority': 0}),
#    Queue('priority_queue', priority_exchange, routing_key='priority_queue', consumer_arguments={'x-priority': 10}),
# )
# CELERY_ROUTES = ({'jwtauth.tasks.test_task': {
#                        'queue': 'priority_queue',
#                        'routing_key': 'priority_queue'
#                }}, )
# CELERY_DEFAULT_QUEUE = 'default'
# CELERY_DEFAULT_EXCHANGE = 'default'
# CELERY_DEFAULT_ROUTING_KEY = 'default'

# EMAIL SETTINGS
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST_USER', 'smtp.gmail.com')
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'no-reply@lockandrent.ru')
