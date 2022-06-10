from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/room/(?P<course_id>\d+)/$', consumers.
            ChatConsumer),
]

"""It is a good practice to prepend WebSocket URLs with /ws/ to 
differentiate them from URLs used for standard synchronous HTTP 
requests. This also simplifies the production setup when an HTTP 
server routes requests based on the path"""
