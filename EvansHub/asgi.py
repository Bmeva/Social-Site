import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EvansHub.settings')
import django
django.setup()
from django.core.asgi import get_asgi_application




from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from Chat.routing import websocket_urlspatterns

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'https': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlspatterns
        )
    ),
})
