"""
ASGI config for boardproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boardproject.settings')

#application = get_asgi_application()
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.routing import URLRouter
from channels.auth import AuthMiddlewareStack
import boardapp.routing
# import boardproject.routing

application = ProtocolTypeRouter( {
    # 'http': django_asgi_app,
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack( URLRouter( boardapp.routing.websocket_urlpatterns ) )
    # 'websocket': AuthMiddlewareStack( URLRouter( boardproject.routing.websocket_urlpatterns ) )
} )

