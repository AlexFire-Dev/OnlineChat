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


class IndexView(TemplateView):
    template_name = 'chat/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        membership = Member.objects.filter(user=self.request.user, active=True, banned=False).order_by('id')

        context.update({
            'membership': membership,
        })
        return context


class GuildView(TemplateView):
    template_name = 'chat/guild.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        guild = get_object_or_404(Guild, id=kwargs.get('guild'))
        member = get_object_or_404(Member, user=self.request.user, guild=guild, active=True, banned=False)
        channel_id = self.request.GET.get('channel')
        guild_channels = Channel.objects.filter(guild=guild).order_by('id').order_by('private')

        if channel_id:
            channel = get_object_or_404(guild_channels, id=channel_id)
        else:
            channel = guild_channels.first()
        messages = Message.objects.filter(channel=channel)

        context.update({
            'guild': guild,
            'member': member,
            'current_channel': channel,
            'channels': guild_channels,
            'messages': messages,
        })
        return context


class GuildCreateView(CreateView):
    form_class = CreateGuildForm
    template_name = 'chat/guild_create.html'

    def form_valid(self, form):
        name = form.cleaned_data.get('name', f'Сервер {self.request.user.username}')

        args = {
            'name': name,
            'creator': self.request.user,
            'poster': self.request.FILES.get('poster'),
        }
        guild = Guild.objects.create(**args)
        Member.objects.create(guild=guild, user=self.request.user, admin=True)
        Channel.objects.create(guild=guild, name='Основной')

        return HttpResponseRedirect(reverse_lazy('guild-chat', args=[guild.id]))


class ChannelCreateView(CreateView):
    form_class = CreateChannelForm
    template_name = 'chat/channel_create.html'

    def get_success_url(self):
        return reverse('guild-chat', args=[self.kwargs.get('guild')])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'guild': get_object_or_404(Guild, id=self.kwargs.get('guild')),
        })
        return context

    def dispatch(self, request, *args, **kwargs):
        guild = get_object_or_404(Guild, id=self.kwargs.get('guild'))
        me = get_object_or_404(Member, guild=guild, user=self.request.user, admin=True, active=True, banned=False)
        if me.user == guild.creator:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('guild-chat', args=[self.kwargs.get('guild')]))

    def form_valid(self, form):
        args = {
            'name': form.cleaned_data.get('name'),
            'guild_id': self.kwargs.get('guild'),
            'private': form.cleaned_data.get('private'),
        }

        Channel.objects.create(**args)
        return HttpResponseRedirect(self.get_success_url())


class GuildJoinView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('index')

    def get(self, request, *args, **kwargs):
        try:
            link = InviteLink.objects.get(key=self.request.GET.get('join-input'))
        except:
            return HttpResponseRedirect(reverse('index'))
        guild = link.guild
        Member.objects.get_or_create(user=self.request.user, guild=guild)
        member = Member.objects.get(user=self.request.user, guild=guild)
        if member.banned:
            return HttpResponseRedirect(reverse('index'))
        member.active = True
        member.save()

        channel_layer = channels.layers.get_channel_layer()
        username = member.user.username
        if member.user.get_full_name():
            username = member.user.get_full_name()
        async_to_sync(channel_layer.group_send)(
            f'guild_{guild.id}',
            {
                'type': 'chat_member_joined',
                'member': {
                    'id': member.id,
                    'user': member.user.id,
                    'username': username,
                    'admin': member.admin,
                    'bot': member.user.bot,
                }
            }
        )

        return super(GuildJoinView, self).get(self, request, *args, **kwargs)


class GuildLeaveView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('index')

    def get(self, request, *args, **kwargs):
        guild = get_object_or_404(Guild, id=self.kwargs.get('guild'))
        me = get_object_or_404(Member, guild=guild, user=self.request.user, active=True, banned=False)
        me.active = False
        me.admin = False
        me.save()

        channel_layer = channels.layers.get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'guild_{guild.id}',
            {
                'type': 'chat_member_left',
                'member': {
                    'id': me.id,
                }
            }
        )

        return super(GuildLeaveView, self).get(self, request, *args, **kwargs)
