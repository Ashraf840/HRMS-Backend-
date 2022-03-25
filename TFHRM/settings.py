"""
Django settings for TFHRM project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
import os.path
import sys

# import environ


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR.as_posix() + 'templates'
STATIC_DIR = BASE_DIR.as_posix() + 'static'
MEDIA_DIR = BASE_DIR.as_posix() + 'media'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^^fv-&)8of=nhg48zj7$u_=i$ju%br7@ioy39010nexw*k5+t='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['0.0.0.0', '44.242.38.198', '127.0.0.1', 'tfhrm.herokuapp.com', 'careeradmin.techforing.com',
#                  'www.careeradmin.techforing.com']
# ALLOWED_HOSTS = ['*']

ALLOWED_HOSTS = [
    '0.0.0.0',
    '44.242.38.198',
    'techforing.com',
    '127.0.0.1',
    '127.0.0.1:8000',
    'localhost:3001',
    'localhost:3000',
    # ===production===
    # 'careeradmin.techforing.com',
    # 'career.techforing.com',
    # 'hrms.techforing.com',
    # ===Dev===
    'devcareeradmin.techforing.com',
    'devcareer.techforing.com',
    'devhrms.techforing.com',
]

# Initialise environment variables
"""
env = environ.Env()
environ.Env.read_env(BASE_DIR.joinpath('.env'))
"""

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Installed Packages
    'rest_framework',
    'rest_framework_simplejwt',
    'django_rest_passwordreset',
    'rest_framework_simplejwt.token_blacklist',
    'django_cleanup',

    # Corsheaders
    'corsheaders',
    'drf_multiple_model',
    'drf_yasg',
    'django_filters',

    # Crontab
    'django_crontab',

    # Installed Apps
    'UserApp',
    'RecruitmentManagementApp',
    'TFHRM_API_App',
    'AdminOperationApp',
    'SupportApp',
    'pdfGenerator',
    'HRM_Admin',
    'HRM_controller',
    'HRM_User',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # whitenoise for heroku hosting
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    # cors header middleware
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Simple JWT’s behavior customization
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'TFHRM.wsgi.application'
ROOT_URLCONF = 'TFHRM.urls'

# ============== sqlite3 Db ==============
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

"""
Local server DB
"""
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


"""
Dev server DB
"""

# ============== mysql Db Production ==============
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'hrm_techforing',
#         'USER': 'root',
#         'PASSWORD': 'ghFGH56$%&',
#         'OPTIONS': {
#             'sql_mode': 'traditional',
#         }
#     }
# }
# ============== mysql Db Development==============
# 'NAME': 'dev_hrm_tf',
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hrm_techforing',
        'USER': 'root',
        'PASSWORD': 'ghFGH56$%&',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    }
}

# ============== securing proxy for hosting ==============
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

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
# Restframework authentication file
REST_FRAMEWORK = {
    # 'DEFAULT_PERMISSION_CLASSES':[
    #     'rest_framework.permissions.IsAuthenticated',
    # ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',

    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ]
}

# DJANGO_REST_PASSWORDRESET_TOKEN_CONFIG = {
#     "CLASS": "django_rest_passwordreset.tokens.RandomNumberTokenGenerator",
#     "OPTIONS": {
#         "min_number": 1500,
#         "max_number": 9999
#     }
# }

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = 'UserApp.User'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
# STATIC_ROOT = BASE_DIR.joinpath('staticfiles')
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.joinpath('staticfiles')
STATICFILES_DIRS = ['static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.joinpath('media')
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ORIGIN_ALLOW_ALL = False
# CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    'http://0.0.0.0',
    'https://44.242.38.198',
    'http://127.0.0.1',
    'http://127.0.0.1:8000',
    'http://localhost:3001',
    'http://localhost:3000',
    'http://localhost:8000',
    # ===production===
    # 'https://careeradmin.techforing.com',
    # 'https://career.techforing.com',
    # 'https://hrms.techforing.com',
    # ===dev===
    'https://devcareeradmin.techforing.com',
    'https://devcareer.techforing.com',
    'https://devhrms.techforing.com',
]

import os

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'pranto.techforing@gmail.com'
EMAIL_HOST_PASSWORD = 'tehctrahgvpjsuoz'

# Plivo access
# PLIVO_ID = 'MAOGQ0MZI1MTMZYZC4YW'
# AUTH_TOKEN = 'N2JmMDljMjFmYmNkMDRjZDI5ODYwMzQ3OGU5NzRh'
# SENDER_ID = '+1 904-207-7424'

# Crontab
CRONJOBS = [
    ('0 0 * * *', 'HRM_User.cron.attendance_data'),
    ('0 0 15 1 *', 'HRM_User.cron.create_holiday'),
]
