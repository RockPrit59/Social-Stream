import os
import django
from django.core.asgi import get_asgi_application

# 1. Set settings and Initialize Django FIRST
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django_asgi_app = get_asgi_application()

# 2. NOW import the routing and channels tools
# (These imports must happen AFTER get_asgi_application is called)
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import feed.routing

# 3. Define the Application
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            feed.routing.websocket_urlpatterns
        )
    ),
})