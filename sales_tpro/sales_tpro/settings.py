from pathlib import Path
import environ
import os

# Инициализация переменных окружения
env = environ.Env()
environ.Env.read_env()  # Чтение переменных из .env файла

# Настройки проекта
BASE_DIR = Path(__file__).resolve().parent.parent


# Секретный ключ
SECRET_KEY = env('SECRET_KEY', default='fallback-secret-key')

# Отладочный режим
DEBUG = env.bool('DEBUG', default=True)

# Разрешенные хосты
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# Настройки базы данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME', default='salesdb'),
        'USER': env('DB_USER', default='salesuser'),
        'PASSWORD': env('DB_PASSWORD', default='Volume632'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='5432'),
    }
}

# Настройки безопасности
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)  # Перенаправление на HTTPS
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=False)  # Защита CSRF через HTTPS
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=False)  # Защита сессий через HTTPS

# Приложения Django
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sales_project',
    # Добавьте дополнительные приложения по мере необходимости
]

# Миддлвары
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Конфигурация корневого URL
ROOT_URLCONF = 'sales_tpro.urls'



# Настройки шаблонов
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

# WSGI-приложение
WSGI_APPLICATION = 'sales_tpro.wsgi.application'

# Валидация паролей
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

# Интернационализация
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Статические файлы (CSS, JavaScript, изображения)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Медиафайлы (загружаемые пользователями файлы)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Автоматическое поле для новых моделей
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки для поиска статических файлов
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Автоматическая настройка для авторизации
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
