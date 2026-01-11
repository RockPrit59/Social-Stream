import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# We will create this 'consumers' file in the next step
from feed import consumers 

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/notifications/", consumers.NotificationConsumer.as_asgi()),
            path("ws/chat/<str:username>/", consumers.ChatConsumer.as_asgi()),
        ])
    ),
})