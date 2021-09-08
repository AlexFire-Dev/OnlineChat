import json

import channels.layers
from asgiref.sync import async_to_sync
from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, RedirectView

from .models import *
from .forms import *


def AccountView(request):

    context = {
        'accountuser': request.user,
    }

    return render(request, 'user/profile.html', context=context)


class ProfileChangeView(UpdateView):
    form_class = ProfileChangeForm
    template_name = 'user/profile-change.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'accountuser': self.request.user,
        })
        return context

    def get_success_url(self):
        url = reverse('profile')
        return url
