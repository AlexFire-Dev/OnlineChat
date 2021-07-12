from django.urls import re_path, path

from . import consumers


websocket_urlpatterns = [
    path('ws/chat/<int:guild_id>/', consumers.GuildConsumer.as_asgi()),
]
