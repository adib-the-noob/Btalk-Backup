from pathlib import Path

import os, dotenv
from dotenv import load_dotenv

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ueri0$7fc4(on$len@_#5c1z3uq)+vtglk7bg)yx9n3!)uy&6l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "jazzmin",
    'daphne',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # rest framework
    'rest_framework',
    'rest_framework.authtoken',

    # admin

    # storages
    'storages',

    # firebase
    'fcm_django',

    # cors
    'corsheaders',

    # apps
    'authcore',
    'posts',
    'chat',
    'friends',
    'profiles',
    'notifications',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # cors middleware
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware"
]

ROOT_URLCONF = 'btalk.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# WSGI_APPLICATION = 'btalk.wsgi.application'
ASGI_APPLICATION = 'btalk.asgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        "NAME": "btalk-dev-db",
        "HOST": "localhost",
        "PORT": "5432",
        "USER": "postgres",
        "PASSWORD": "postgres"
    }
}

# auth users Model
AUTH_USER_MODEL = 'authcore.User'

# # redisc channel layer
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('localhost', 6379)],
        },
    },
}

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels.layers.InMemoryChannelLayer"
#     }
# }

# rest Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ]
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
        'authcore.custom_authenticator.authentication_backends.EmailOrPhoneBackend',
        'django.contrib.auth.backends.ModelBackend',
    )

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# media
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# OTP handler
OTP_HANDLER_API_KEY = os.getenv("OTP_HANDLER_API_KEY")


# Celery settings
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"

# aws settings
AWS_ACCESS_KEY_ID = "AKIAV22M6BZ5UC2W4TTD"
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "btalk-dev-bucket"
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_REGION_NAME = "ap-south-1"
AWS_S3_FILE_OVERWRITE = True
AWS_DEFAULT_ACL = None
AWS_S3_VERITY = True
AWS_S3_CUSTOM_DOMAIN = "d1s1i0e6ao95bj.cloudfront.net"
AWS_CLOUDFRONT_DISTRIBUTION_ID="E2MU9DBXML78KC"
# s3 static settings
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"


# # FCM_DJANGO_SETTINGS
# # run export GOOGLE_APPLICATION_CREDENTIALS="credentials.json" in terminal
# GOOGLE_APPLICATION_CREDENTIALS = "credentials.json"
FCM_DJANGO_SETTINGS = {
    "FCM_SERVER_KEY": "AAAAyUbFO8M:APA91bHGD8PeoCZSl2ifPmVSl1mWFOiXSuiyguUNt62aoGRkKOO2FFKJdEFFV5yPkb90AP1-aS3Rkf0rk-dq4eYmes0umcgOlI5BbUdutEX-cMo3dmBbKn4cqO3BMSALgp1IpuvsU835",
}

# cors settings
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

# Access-Control-Allow-Credentials: true
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = [
    'http://localhost:9000',
    "http://localhost:8080",
    "http://127.0.0.1:9000",
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://127.0.0.1"

    # Add any other allowed origins here
]

CORS_ALLOW_HEADERS = (
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
)

# fcm
from firebase_admin import initialize_app, credentials
from google.auth import load_credentials_from_file
from google.oauth2.service_account import Credentials

# create a custom Credentials class to load a non-default google service account JSON
class CustomFirebaseCredentials(credentials.ApplicationDefault):
    def __init__(self, account_file_path: str):
        super().__init__()
        self._account_file_path = account_file_path

    def _load_credential(self):
        if not self._g_credential:
            self._g_credential, self._project_id = load_credentials_from_file(self._account_file_path,
                                                                              scopes=credentials._scopes)

# init default firebase app
# this loads the default google service account with GOOGLE_APPLICATION_CREDENTIALS env variable
FIREBASE_APP = initialize_app()

# init second firebase app for fcm-django
# the environment variable contains a path to the custom google service account JSON
custom_credentials = CustomFirebaseCredentials(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
FIREBASE_MESSAGING_APP = initialize_app(custom_credentials, name='messaging')

FCM_DJANGO_SETTINGS = {
    "DEFAULT_FIREBASE_APP": FIREBASE_MESSAGING_APP,
    # [...] your other settings
}

# admin panel 
JAZZMIN_SETTINGS = {
    "site_title": "Btalk Admin",
    "site_header": "Btalk Admin",
    "site_brand": "Btalk Admin",
    "navigation_expanded": False,

}

JAZZMIN_SETTINGS["show_ui_builder"] = True


# twilio
# twilio configuations
TWILIO_ACCOUNT_SID = os.getenv('ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('AUTH_TOKEN')
COUNTRY_CODE = os.getenv('COUNTRY_CODE')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')