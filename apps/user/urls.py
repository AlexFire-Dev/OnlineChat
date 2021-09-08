import django.contrib.auth.views as django_views

from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy, include
from django_registration.backends.activation.views import RegistrationView

from .views import *
from .forms import RegisterForm


urlpatterns = [
    url('', include('social_django.urls', namespace='social')),
    path('api-auth/', include('rest_framework.urls')),

    path('register/', RegistrationView.as_view(form_class=RegisterForm, success_url=reverse_lazy('django_registration_complete')), name='register'),
    path('', include('django_registration.backends.activation.urls')),

    path('me/', login_required(AccountView), name='profile'),
    path('change/', login_required(ProfileChangeView.as_view()), name='profile-change'),

    path('login/', django_views.LoginView.as_view(), name='login'),
    path('logout/', django_views.LogoutView.as_view(), name='logout'),
    path('password_change/', django_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', django_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', django_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', django_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', django_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', django_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
