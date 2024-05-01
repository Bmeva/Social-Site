from django.urls import re_path
from Chat import consumer

websocket_urlspatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumer.ChatConsumer.as_asgi()),
    re_path(r'ws/group-chat/(?P<room_name>[\w-]+)/$', consumer.ChatConsumer.as_asgi()),


]

