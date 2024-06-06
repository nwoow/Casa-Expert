
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from account.routing import websocket_urlpatterns
from account.middlewareauth import JWTAuthMiddlewareStack
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'casaxprt.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":JWTAuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        ),
    )     
})