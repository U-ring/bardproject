from django.urls import path
# from channels.auth import AuthMiddlewareStack
# from . import consumers
# from .consumers import consumers
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path( 'ws/chat/', ChatConsumer.as_asgi() ),
    # re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    # url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer.as_asgi()),
]