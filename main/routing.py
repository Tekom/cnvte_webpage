from django.urls import path 
from .consumer import GraphConsumer

ws_urlpatterns = [
    path('ws/live_data/', GraphConsumer.as_asgi()),
]