import os
from pathlib import Path

from celery.schedules import crontab
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR.parent / 'infra_bt/.env')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'FALSE').upper() == 'TRUE'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1').split(',')

CSRF_TRUSTED_ORIGINS = [
    'http://94.241.143.166',
    'https://better-together.tw1.ru',
    'http://localhost:8000',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'django_filters',
    'django_object_actions',
    'djoser',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    'taggit',
    'gmailapi_backend',
    'api.apps.ApiConfig',
    'content.apps.ContentConfig',
    'notifications.apps.NotificationsConfig',
    'projects.apps.ProjectsConfig',
    'users.apps.UsersConfig',
    'corsheaders',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'rest_framework.middleware.AuthenticationMiddleware',
    # 'rest_framework.middleware.AuthorizationMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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
            'libraries': {
                'staticfiles': 'django.templatetags.static',
            },
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'volunteers'),
        'USER': os.getenv('POSTGRES_USER', 'volunteers_user'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', 5432),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        },
    },
    {
        'NAME': 'users.validators.PasswordMaximumLengthValidator',
        'OPTIONS': {'max_length': 20},
    },
    {
        'NAME': 'users.validators.PasswordRegexValidator',
        'OPTIONS': {
            'regex': r"(^[%!#$&*'+/=?^_;():@,.<>`{|}~-«»0-9A-ZА-ЯЁ]+)\Z",
        },
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = Path(BASE_DIR, 'collected_static')

MEDIA_URL = 'media/'
MEDIA_ROOT = Path(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 6,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DATETIME_FORMAT': "%d.%m.%Y %H:%M",
    # 'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

DJOSER = {
    'LOGIN_FIELD': 'email',
    'HIDE_USERS': False,
    'USER_CREATE_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_URL': '#/login/password-reset/{uid}/{token}',
    'ACTIVATION_URL': '#/login/password-activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND': True,
    'SERIALIZERS': {
        'current_user': 'api.serializers.CurrentUserSerializer',
        'token_create': 'users.auth.serializers.CustomTokenCreateSerializer',
        'password_reset': 'users.auth.serializers.CustomSendEmailResetSerializer',
        'set_password': 'users.auth.serializers.CustomSetPasswordSerializer',
    },
}

EMAIL_BACKEND = 'gmailapi_backend.mail.GmailBackend'
GMAIL_API_CLIENT_ID = os.getenv('GMAIL_API_CLIENT_ID', '')
GMAIL_API_CLIENT_SECRET = os.getenv('GMAIL_API_CLIENT_SECRET', '')
GMAIL_API_REFRESH_TOKEN = os.getenv('GMAIL_API_REFRESH_TOKEN', '')

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://94.241.143.166:3000',
    'http://better-together.tw1.ru/',
    'https://better-together.tw1.ru/',
]

CORS_ORIGIN_ALLOW_ALL = os.getenv('DEBUG', 'FALSE').upper() == 'TRUE'

AUTH_USER_MODEL = 'users.User'

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {  # авторизация в джанго по токену
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Use your token in the following format: <strong>Token <em>&lt;your-token&gt;</em></strong> ',
        },

        # 'Basic': {'type': 'basic'},  # базова авторизация
    },
    'USE_SESSION_AUTH': True,  # кнопка джанго логин можно отключить поменяв False
    'JSON_EDITOR': True,
    'SHOW_REQUEST_HEADERS': True,
    'DEFAULT_MODEL_RENDERING': 'model',  # Отображение моделей (model, example)
    # Глубина отображения моделей (-1 - без ограничений)
    'DEFAULT_MODEL_DEPTH': 2,
    'DOC_EXPANSION': 'list',  # full, none
    'OPERATIONS_SORTER': 'alpha',  # Сортировка операций (alpha, method)
    'TAGS_SORTER': 'alpha',  # Сортировка тегов (alpha, order)
}

CELERY_BROKER_URL = 'redis://redis:6379/1'
CELERY_RESULT_BACKEND = 'redis://redis:6379/2'

CELERY_BEAT_SCHEDULE = {
    'delete_not_active_users': {
        'task': 'users.tasks.delete_not_active_users',
        'schedule': crontab(hour=20, minute=45),
    },
}

# Constants
# MAX_LENGTH_NAME = 50
MAX_LENGTH_SLUG = 50
MAX_LENGTH_PASSWORD = 20
MAX_LENGTH_EMAIL = 256
MIN_LENGTH_EMAIL = 6
MAX_LENGTH_EMAIL_USER_PART = 64
MESSAGE_EMAIL_NOT_VALID = 'Некорректный email!'
MESSAGE_EMAIL_USER_PART_VALID = f'Максимальная длинна пользовательской части: {MAX_LENGTH_EMAIL_USER_PART} символа.'

MAX_LEN_CHAR = 250
LEN_PHONE = 12
MAX_LEN_TEXT_IN_ADMIN = 50

MAX_LEN_NAME = 100
MIN_LEN_NAME_PROJECT = 2
MAX_LEN_NAME_PROJECT = 150
MAX_LEN_SLUG = 50
LEN_OGRN = 13
MESSAGE_PHONE_REGEX = (
    f'Номер должен начинаться с +7, и содержать {LEN_PHONE} символов. Вторая цифра в номере не может быть 0'
)
MESSAGE_EMAIL_VALID = (
    f'Длина поля от {MIN_LENGTH_EMAIL} до {MAX_LENGTH_EMAIL} символов'
)

ORGANIZATION = ' {} ОГРН: {} {}'
VOLUNTEER = 'Пользователь: {} Город: {} Навыки: {}'
PROJECT = 'Название: {}, Организатор: {}, Категория: {}, Город: {}'
PROJECTPARTICIPANTS = 'Проект: {} Волонтер: {}'
PROJECTINCOMES = 'Проект: {} Волонтер: {} Стаутс заявки {}'

MIN_LEN_TEXT_FEEDBACK = 10
MAX_LEN_TEXT_FEEDBACK = 750
MESSAGE_TEXT_FEEDBACK_VALID = f'Длина поля от {MIN_LEN_TEXT_FEEDBACK} до {MAX_LEN_TEXT_FEEDBACK} символов'

MIN_LEN_NAME_USER = 2
MAX_LEN_NAME_USER = 40
MESSAGE_NAME_USER_VALID = (
    f'Длина поля от {MIN_LEN_NAME_USER} до {MAX_LEN_NAME_USER} символов'
)
MESSAGE_NAME_USER_CYRILLIC = 'Введите имя кириллицей'

MIN_LEN_TITLE = 2
MAX_LEN_TITLE = 100
MESSAGE_TITLE_VALID = (
    f'Длина поля от {MIN_LEN_TITLE} до {MAX_LEN_TITLE} символов'
)
MESSAGE_TITLE_CYRILLIC = 'Введите название кириллицей'

OGRN_ERROR_MESSAGE = 'ОГРН должен состоять из 13 цифр.'
MAX_LENGTH_ROLE = 50
MIN_LEN_TELEGRAM = 5
MAX_LEN_TELEGRAM = 32
TELEGRAM_ERROR_MESSAGE = (
    f'Ник в Telegram должен начинаться с @ и содержать только буквы, цифры и знаки подчеркивания. '
    f'Длина поля от {MIN_LEN_TELEGRAM} до {MAX_LEN_TELEGRAM} символов.'
)

VALUATIONS_ON_PAGE_ABOUT_US = 4


MIN_LEN_TEXT_FIELD_V1 = 2
MIN_LEN_TEXT_FIELD_V2 = 10
MAX_LEN_TEXT_FIELD = 750

MIN_LEN_ABOUT_US = 10
MAX_LEN_ABOUT_US = 750
MESSAGE_ABOUT_US_VALID = (
    f'Длина поля от {MIN_LEN_ABOUT_US} до {MAX_LEN_ABOUT_US} символов'
)
MESSAGE_ABOUT_US_REGEX_VALID = """Допускаются цифры, буквы, пробелы и спецсимволы: %% №\\!#$&*'+/=?^_;():@,.<>`{|}[]~-«»"""

MAX_LEN_PHOTOS = 10
MIN_LEN_COVER_LETTER = 10
MAX_LEN_COVER_LETTER = 530
MESSAGE_COVER_LETTER_VALID = (
    f'Длина поля от {MIN_LEN_COVER_LETTER} до {MAX_LEN_COVER_LETTER} символов'
)
