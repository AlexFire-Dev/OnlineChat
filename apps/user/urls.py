import django.contrib.auth.views as django_views

from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy, include

from .views import *


urlpatterns = [
    url('', include('social_django.urls', namespace='social')),
    path('api-auth/', include('rest_framework.urls')),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', django_views.LogoutView.as_view(), name='logout'),

    path('password_change/', django_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', django_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', django_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', django_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', django_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', django_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
