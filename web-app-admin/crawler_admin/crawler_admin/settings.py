"""
Django settings for crawler_admin project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
import sys
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

if os.getenv("DATABASE_DRIVER") == 'mysql':
    import pymysql 
    pymysql.install_as_MySQLdb()
    

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("APP_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.getenv("APP_DEBUG") == 'True' else False

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': 'sql.log',
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }


ALLOWED_HOSTS=['*']
# ALLOWED_HOSTS = ['localhost','http://127.0.0.1:8000', 'http://localhost:8080']

# Application definition
INSTALLED_APPS = [
    "corsheaders",
    # add rest_framework support to the project
    "rest_framework",
    # "modules.simpleui.apps.SimpleApp",
    "fontawesomefree",
    'modules.jazzmin.apps.JazzminConfig', 
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    "mptt",
    "import_export",
    "django_filters",
    "modules.crawler.apps.ScrapersConfig",
]

if os.getenv("APP_ENV") == "production":
    S3_BUCKET_NAME = "pcw-dev-admin"
    STATICFILES_STORAGE = "django_s3_storage.storage.StaticS3Storage"
    AWS_S3_BUCKET_NAME_STATIC = S3_BUCKET_NAME
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % S3_BUCKET_NAME
    STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
    INSTALLED_APPS.append("django_s3_storage")
else:
    STATIC_URL = "static/" 

MIDDLEWARE = [ 
    # Default
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', 
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
      # CORS
    # "corsheaders.middleware.CorsMiddleware",
    # "django.middleware.common.CommonMiddleware", 
    # "corsheaders.middleware.CorsPostCsrfMiddleware",

    "modules.crawler.middleware.cors_middleware.CorsMiddlewareCustom",
]
 


ROOT_URLCONF = "crawler_admin.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "crawler_admin.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.{}".format(os.getenv("DATABASE_DRIVER")),
        "HOST": os.getenv("DATABASE_HOST"),
        "PORT": os.getenv("DATABASE_PORT"),
        "NAME": os.getenv("DATABASE_NAME"),
        "USER": os.getenv("DATABASE_USER"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD"),
        'OPTIONS': {
            'sql_mode': 'traditional',
        } if os.getenv("DATABASE_DRIVER") == "mysql" else {}
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'djongo',
#         'NAME': os.getenv('DATABASE_NAME'),
#         'CLIENT': {
#             'host': '{}://{}:{}/{}?directConnection=true'.format(os.getenv('DATABASE_DRIVER'), os.getenv('DATABASE_HOST'), os.getenv('DATABASE_PORT'), os.getenv('DATABASE_NAME')),
#             # 'username': os.getenv('DATABASE_USER'),
#             # 'password': os.getenv('DATABASE_PASSWORD'),
#             # 'authSource': 'admin',
#             # 'authMechanism': 'SCRAM-SHA-1',
#         }
#     }
# }
# print('DATABASES', DATABASES)

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
 
# STATICFILES_DIRS = [
#     BASE_DIR / "static",
#     # '/var/www/static/',
# ]

# All settings common to all environments
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(BASE_DIR, "static")
  
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CORS_ALLOW_ALL_ORIGINS = True  
# CORS_ORIGIN_ALLOW_ALL = False
# CORS_ORIGIN_WHITELIST = ['http://localhost:8080',]
# CORS_ALLOWED_ORIGINS = ['http://localhost:8080',]
# CORS_ALLOWED_ORIGIN = ["127.0.0.1", 'localhost','localhost:8080', 'http://localhost:8080/', 'http://127.0.0.1', 'http://localhost']
# CORS_ALLOWED_ORIGIN = ['localhost:8080', 'http://localhost:8080/', 'http://127.0.0.1', 'http://localhost']
REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 20,
}
# CORS_ALLOWED_ORIGINS = [
#     "https://example.com",
#     "https://sub.example.com",
#     "http://localhost:8080",
#     "http://127.0.0.1:9000",
# ]
# CORS_ALLOW_METHODS = [
#     "DELETE",
#     "GET",
#     "OPTIONS",
#     "PATCH",
#     "POST",
#     "PUT",
# ]

# CORS_ALLOW_HEADERS = [
#     "accept",
#     "accept-encoding",
#     "authorization",
#     "content-type",
#     "dnt",
#     "origin",
#     "user-agent",
#     "x-csrftoken",
#     "x-requested-with",
# ]

# CSRF_TRUSTED_ORIGINS = [
#     "http://localhost:8080",
# ]
