"""
ASGI config for cnvte_webpage project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cnvte_webpage.settings')
django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from django.urls import path
from main.consumer import GraphConsumer
import logging

def get_module_logger(mod_name):
    """
    To use this, do logger = get_module_logger(__name__)
    """
    logger = logging.getLogger(mod_name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger

get_module_logger(__name__).info(f'asgi server')
# from main.routing import ws_urlpatterns



ws_urlpatterns = [
    path('ws/live_data/', GraphConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'http':django_asgi_app,
    'websocket': AuthMiddlewareStack(
                    URLRouter(
                        ws_urlpatterns
    ))
}) 

