from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy, include

from .views import *


urlpatterns = [
    path('', login_required(IndexView.as_view()), name='index'),

    path('guild/join/', login_required(GuildJoinView.as_view()), name='guild-join'),
    path('guild/<int:guild>/', login_required(GuildView.as_view()), name='guild-chat'),
    path('guild/<int:guild>/leave/', login_required(GuildLeaveView.as_view()), name='guild-leave'),

    path('guild/<int:guild>/create/', login_required(ChannelCreateView.as_view()), name='channel-create'),

    path('guild/create/', login_required(GuildCreateView.as_view()), name='guild-create'),
]
