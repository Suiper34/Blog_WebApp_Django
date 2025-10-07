from os import environ

from django.core.asgi import get_asgi_application

environ.setdefault('DJANGO_SETTINGS_MODULE',
                   'blog_webapp_django.config.settings')

application = get_asgi_application()
