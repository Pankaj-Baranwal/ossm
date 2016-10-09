import datetime
import dj_database_url
import os


BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

STAGING = 'STAGING' in os.environ
PRODUCTION = 'PRODUCTION' in os.environ

SECRET_KEY = '&p1c8n_y5efqa5(u9byuutsuj#bbc0$x=fdkcec+8gd45npup#'
DEBUG = not PRODUCTION
ALLOWED_HOSTS = ['*']
INTERNAL_IPS = ['127.0.0.1', ]


INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'anymail',
    'landing',
    'ossm',
    'people',
    'events',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.windowslive',
    'allauth.socialaccount.providers.facebook',
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_auth.registration',
    'rest_framework_swagger',
    'storages',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

ANYMAIL = {
    'MAILGUN_API_KEY': os.environ.get('MG_API_KEY'),
    'MAILGUN_SENDER_DOMAIN': os.environ.get('MG_SERVER_DOMAIN'),
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

SWAGGER_SETTINGS = {
    'JSON_EDITOR': True,
    'APIS_SORTER': 'alpha',
    'OPERATIONS_SORTER': 'method',
    'SHOW_REQUEST_HEADERS': True,
    'VALIDATOR_URL': None,
}

JWT_EXPIRATION_DELTA = 3000 if DEBUG else 86400
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=JWT_EXPIRATION_DELTA)
}

EMAIL_BACKEND = 'anymail.backends.mailgun.MailgunBackend'
DEFAULT_FROM_EMAIL = 'noobz@convoke.io'

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ossm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
        ],
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

WSGI_APPLICATION = 'ossm.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


if not DEBUG:
  AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
  ]

SITE_ID = 1

AUTH_USER_MODEL = 'people.User'

SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_PROVIDERS = {
  'facebook': {
    'METHOD': 'oauth2',
    'SCOPE': ['email', 'public_profile'],
  }
}

# allauth config

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http' if DEBUG else 'https'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

REST_USE_JWT = True

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'public'),  # brunch builds
]

LOGIN_REDIRECT_URL = '/dashboard/'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'verbose_console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': os.getenv('LOG_LEVEL', 'DEBUG'),
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': os.getenv('LOG_LEVEL', 'INFO'),
        },
        'django': {
            'handlers': ['console'],
            'level': os.getenv('LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'django.request': {
            'handlers': ['verbose_console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

if PRODUCTION or STAGING:
    DEBUG = False
    CSRF_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SESSION_COOKIE_SECURE = True

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    SITE_URL = os.environ['HEROKU_URL']
    SECRET_KEY = os.environ['SECRET_KEY']
    ALLOWED_HOSTS = ['.herokuapp.com', SITE_URL, ('.%s' % SITE_URL)]
    DATABASES = {'default': dj_database_url.config()}

    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_S3_CUSTOM_DOMAIN = r'%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    AWS_HEADERS = {
        'Cache-Control': 'max-age=%d' % (60 * 60 * 24 * 15),    # NOTE (@prashnts): 15 days.
    }
    AWS_IS_GZIPPED = True
    GZIP_CONTENT_TYPES = (
        'text/css',
        'text/javascript',
        'application/javascript',
        'application/x-javascript',
        'image/svg+xml',
        'application/octet-stream'
    )
    STATIC_URL = r"https://%s/" % AWS_S3_CUSTOM_DOMAIN
    STATIC_ROOT = r"https://%s/" % AWS_S3_CUSTOM_DOMAIN
    STATICFILES_STORAGE = 'ossm.storage.StaticS3Storage'
