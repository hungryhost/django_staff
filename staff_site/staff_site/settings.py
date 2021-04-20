import os
import environ
from pathlib import Path
from datetime import timedelta
from celery.schedules import crontab
from kombu import Exchange, Queue

# finding a root directory of the project
root = environ.Path(__file__) - 2

# setting roots for static, media, templates
templates_root = root('templates')

env = environ.Env()
# reading env file
environ.Env.read_env(env_file=root('.env'))
# site root points to rentAccess root folder
SITE_ROOT = root()
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
DEBUG = env.bool('DEBUG', default=False)
SECRET_KEY = env.str('SECRET_KEY')
ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(",")
ADMINS = env.list("ADMINS", default=[('Yury Borodin', 'yuiborodin@lockandrent.ru')])

CORS_ORIGIN_ALLOW_ALL = env.bool('CORS_ORIGIN_ALLOW_ALL', default=True)

CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS')

USE_REDIS_CACHE = env.bool('USE_REDIS_CACHE', default=False)
if USE_REDIS_CACHE:
	CACHE_TTL = 60 * 1

	CACHES = {
		"default": {
			"BACKEND": "django_redis.cache.RedisCache",
			"LOCATION": env('CACHE_URL_1'),
			"OPTIONS": {
				"CLIENT_CLASS": "django_redis.client.DefaultClient",
			},
			"KEY_PREFIX": "lr_cache"
		}
	}
	SESSION_ENGINE = "django.contrib.sessions.backends.cache"
	SESSION_CACHE_ALIAS = "default"
else:
	CACHE_TTL = 60 * 1
	CACHES = {
		'default': {
			'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
		}
	}
	SESSION_CACHE_ALIAS = "default"

INSTALLED_APPS = [
	'django.contrib.staticfiles',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.sites',
	'django.contrib.admin',
	'watchman',
	'backendIntegrations',
	'encrypted_fields',
	'crispy_forms',
	'userAccount',
	'manufacturing',
	'django_filters',
	'django_countries',
	'storages',
	'phone_field',
	'timezone_field',
	'corsheaders',
	'django_otp',
	'django.contrib.admindocs',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_hotp',
    'django_otp.plugins.otp_static',
	'two_factor',
	'twoFactor',

]
SETTINGS_PATH = os.path.normpath(os.path.dirname(__file__))

SITE_ID = 1
MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'corsheaders.middleware.CorsMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django_otp.middleware.OTPMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',

]
AUTH_USER_MODEL = 'userAccount.InternalUser'
LOGIN_REDIRECT_URL = 'lr-main'
LOGIN_URL = 'login'
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
CITIES_LIGHT_TRANSLATION_LANGUAGES = ['ru', 'en', 'abbr']
CITIES_LIGHT_INCLUDE_COUNTRIES = ['RU']
CITIES_LIGHT_INCLUDE_CITY_TYPES = ['PPL', 'PPLA', 'PPLA2', 'PPLA3', 'PPLA4', 'PPLC', 'PPLF', 'PPLG', 'PPLL', 'PPLR',
								   'PPLS', 'STLMT', ]

# Databases
if not DEBUG:
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql',
			'NAME': env("DB_NAME"),
			"USER": env("DB_USER"),
			"PASSWORD": env("DB_PASSWORD"),
			"HOST": env("DB_HOST"),
			"PORT": env("DB_PORT"),
			"OPTIONS": {
				'options': '-c search_path=internal'
			}
		},
		'lr_backend_main': {
			'ENGINE': 'django.db.backends.postgresql',
			'NAME': env("DB_NAME"),
			"USER": env("DB_USER"),
			"PASSWORD": env("DB_PASSWORD"),
			"HOST": env("DB_HOST"),
			"PORT": env("DB_PORT"),
			"OPTIONS": {
				'options': '-c search_path=main'
			}
		}
	}
else:
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.sqlite3',
			'NAME': 'db.sqlite3',
		},
		'lr_backend_main': {
			'ENGINE': 'django.db.backends.sqlite3',
			'NAME': 'C:/web-294/web-294/rentAccess/db.sqlite3',
		}
	}
DATABASE_ROUTERS = ['staff_site.integration_db_router.IntegrationRouter']
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

################################################
# when DEBUG == True DRF will render errors as html pages
USE_S3 = env.bool('USE_S3', default=False)
if USE_S3:
	AWS_ACCESS_KEY_ID = env.str('AWS_ACCESS_KEY_ID')
	AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ACCESS_KEY')
	AWS_STORAGE_BUCKET_NAME = env.str('AWS_STORAGE_BUCKET_NAME')
	AWS_DEFAULT_ACL = 'public-read'
	AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
	AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
	# s3 static settings
	AWS_LOCATION = 'static'
	STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
	STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
	# s3 public media settings
	PUBLIC_MEDIA_LOCATION = 'media'
	MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
	DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

else:
	STATIC_URL = '/static/'
	STATIC_ROOT = '/static/'
	MEDIA_ROOT = os.path.join('media')
	MEDIA_URL = '/media/'

# Static root and file definitions
STATICFILES_DIRS = [
	root("static"),
]
FIELD_ENCRYPTION_KEYS = env("LOCK_ENCRYPTION_KEYS").split(",")
KEY_HASH = env.str('KEY_HASH')
CARD_HASH = env.str('CARD_HASH')
CELERY_BROKER_URL = env.str("CELERY_BROKER_URL", default='redis://127.0.0.1:6379')
CELERY_RESULT_BACKEND = env.str('CELERY_RESULT_BACKEND', default='redis://127.0.0.1:6379')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Moscow'

# default_exchange = Exchange('default', type='direct')
# priority_exchange = Exchange('priority_queue', type='direct')

# CELERY_QUEUES = (
#	Queue('default', default_exchange, routing_key='default', consumer_arguments={'x-priority': 0}),
#	Queue('priority_queue', priority_exchange, routing_key='priority_queue', consumer_arguments={'x-priority': 10}),
# )
# CELERY_ROUTES = ({'jwtauth.tasks.test_task': {
#						'queue': 'priority_queue',
#						'routing_key': 'priority_queue'
#				}}, )
# CELERY_DEFAULT_QUEUE = 'default'
# CELERY_DEFAULT_EXCHANGE = 'default'
# CELERY_DEFAULT_ROUTING_KEY = 'default'

# EMAIL SETTINGS
SERVER_EMAIL = 'server@lockandrent.ru'
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')

# TEMPLATE_PREVIEW_DIR = root('templates')
