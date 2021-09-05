from django.contrib import admin

from .models import *


@admin.register(Guild)
class GuildAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'guild', 'user', 'admin', 'active', 'banned')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'author')


@admin.register(InviteLink)
class InviteLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'guild', 'key')
