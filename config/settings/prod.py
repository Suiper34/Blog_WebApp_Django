from os import environ, path
from pathlib import Path

from .base import *

# production settings

BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

DEBUG: bool = False

ALLOWED_HOSTS: list[str] = environ.get('ALLOWED_HOSTS', '').split(',')

# db configuration
DATABASES: dict[str, dict[str, str]] = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': environ.get('DB_NAME'),
        'USER': environ.get('DB_USER'),
        'PASSWORD': environ.get('DB_PASSWORD'),
        'HOST': environ.get('DB_HOST', 'localhost'),
        'PORT': environ.get('DB_PORT', '5432'),
    }
}

AUTH_USER_MODEL = 'users.User'

# static files path
STATIC_URL: str = '/static/'
STATIC_ROOT: str = path.join(BASE_DIR, 'staticfiles')

# media files
MEDIA_URL: str = '/media/'
MEDIA_ROOT: str = path.join(BASE_DIR, 'media')

# security settings
SECURE_BROWSER_XSS_FILTER: bool = True
SECURE_CONTENT_TYPE_NOSNIFF: bool = True
SECURE_SSL_REDIRECT: bool = True
SESSION_COOKIE_SECURE: bool = True
CSRF_COOKIE_SECURE: bool = True
SECURE_HSTS_SECONDS: int = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS: bool = True
SECURE_HSTS_PRELOAD: bool = True

# Email settings
EMAIL_BACKEND: str = environ.get(
    'EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST: str = environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT: int = int(environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS: bool = environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER: str | None = environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD: str | None = environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL: str = environ.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)
