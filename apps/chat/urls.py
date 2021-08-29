from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy, include

from .views import *


urlpatterns = [
    # path('', login_required(IndexView.as_view()), name='index'),
    path('', IndexView.as_view(), name='index'),
]