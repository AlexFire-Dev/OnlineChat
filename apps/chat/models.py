from django.db import models

import random
import string

from apps.user.models import User


class Guild(models.Model):
    name = models.CharField(max_length=30)
    poster = models.ImageField(upload_to='images/guilds/posters', blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='guilds')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.name

    def GenerateKey(self):
        letters = string.ascii_lowercase
        key = ''.join(random.choice(letters) for i in range(30))
        InviteLink.objects.create(guild=self, key=key)


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='memberships')
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE, related_name='members')
    admin = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    banned = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.guild}: {self.user}'


class Channel(models.Model):
    name = models.CharField(max_length=30)
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE, related_name='channels')
    private = models.BooleanField(default=False)


class Message(models.Model):
    author = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='persons_messages')
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='channels_messages')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}: {self.text}'


class InviteLink(models.Model):
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE, related_name='invitation_links')
    key = models.CharField(max_length=30, unique=True, null=True)

    def __str__(self):
        return f'{self.guild}: {self.key}'
