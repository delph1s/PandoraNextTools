"""
module description:

django settings
"""

import sys
import os
import datetime
import shutil
from pathlib import Path

from django.utils.translation import gettext_lazy as _


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


CONFIG_FILE_PATH = BASE_DIR / 'conf' / 'config.py'
CONFIG_EXAMPLE_FILE_PATH = BASE_DIR / 'conf' / 'config.example.py'
if CONFIG_FILE_PATH.is_file():
    from conf.config import *
else:
    shutil.copy(CONFIG_EXAMPLE_FILE_PATH, CONFIG_FILE_PATH)
    from conf.config import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = locals().get(
    'SECRET_KEY', "django-insecure-00000000000000000000000000000000000000000000000000"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = locals().get('DEBUG', True)

ALLOWED_HOSTS = locals().get('ALLOWED_HOSTS', ['*'])


# 项目属性

DJANGO_PROJECT_NAME = locals().get('DJANGO_PROJECT_NAME', 'project')


# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    'rest_framework',  # RESTful 风格
    # 自定义app
    'apps.core.apps.CoreConfig',  # 核心 app
    'apps.tbar.apps.PNMConfig',  # pnm app
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "pnts.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = "pnts.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'zh-CN'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = False

USE_TZ = True

LANGUAGES = [
    ('zh-hans', _('Simplified Chinese')),
    ('en', _('English')),
]

if not (BASE_DIR / 'locale').is_dir():
    (BASE_DIR / 'locale').mkdir()

LOCALE_PATHS = [BASE_DIR / 'locale']


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_ROOT = BASE_DIR / 'media'
if not MEDIA_ROOT.is_dir():
    MEDIA_ROOT.mkdir()
MEDIA_URL = '/media/'


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# DjangoRESTFramework Config

REST_FRAMEWORK = {
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",  # 日期时间格式配置
    'DATE_FORMAT': "%Y-%m-%d",  # 日期格式配置
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    # 'DEFAULT_PAGINATION_CLASS': 'apps.core.pagination.CorePagination',  # 分页器
    # 'PAGE_SIZE': 10,  # 分页大小
    # 'EXCEPTION_HANDLER': 'apps.core.exceptions.core_exception_handler',
    # 'DEFAULT_THROTTLE_CLASSES': 'apps.core.throttling.RateThrottle',  # 截断器
    # 'DEFAULT_THROTTLE_RATE': {'visit_rate': '5/m'},  # 访问频率
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    # 'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'rest_framework.authentication.SessionAuthentication',
    #     'rest_framework.authentication.BasicAuthentication',
    # ),
}


# Cors Config

# 跨域允许cookies
CORS_ALLOW_CREDENTIALS = locals().get('CORS_ALLOW_CREDENTIALS', True)
# 允许所有域名
CORS_ORIGIN_ALLOW_ALL = locals().get('CORS_ORIGIN_ALLOW_ALL', True)
# 白名单
CORS_ORIGIN_WHITELIST = locals().get('CORS_ORIGIN_WHITELIST', [])
# 正则表达式白名单
CORS_ORIGIN_REGEX_WHITELIST = locals().get('CORS_ORIGIN_REGEX_WHITELIST', [])
# 默认可以使用的非标准请求头，需要使用自定义请求头时，就可以进行修改
CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'Authorization',
)
# 默认请求方法
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)
