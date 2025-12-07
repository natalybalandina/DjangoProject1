import os
from dotenv import load_dotenv
from pathlib import Path

# Загружаем переменные окружения из .env файла
load_dotenv(override=True)

# Путь к базовой директории проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Безопасный ключ приложения
SECRET_KEY = os.getenv('SECRET_KEY')

# Настройки отладки
DEBUG = True if os.getenv('DEBUG') == "True" else False

CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'False') == 'True'

# Разрешенные хосты
ALLOWED_HOSTS = ["*"]

# Определение приложений
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'catalog',
    'blogs',
    'users',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'config.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #'DIRS': [],
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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


WSGI_APPLICATION = 'config.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('NAME'),
        'USER': os.getenv('USER'),
        'PASSWORD': os.getenv('PASSWORD'),
        'HOST': os.getenv('HOST'),
        'PORT': os.getenv('PORT'),
    }
}


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


AUTH_USER_MODEL = 'users.User'
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'catalog:home'  # Куда перенаправлять после успешного входа
LOGOUT_REDIRECT_URL = 'catalog:home'  # Куда перенаправлять после выхода


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_URL = '/static/'

#STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')  # Замените на нужный SMTP сервер
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 465))  # Порт по умолчанию 465
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'False') == "True"
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'True') == "True"
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')  # Электронная почта пользователя
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')  # Пароль для электронной почты
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png']

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}