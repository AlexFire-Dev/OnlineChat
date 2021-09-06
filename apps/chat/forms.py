from django import forms

from .models import Guild, Channel, Member


class CreateGuildForm(forms.ModelForm):
    class Meta:
        model = Guild
        fields = ('name', 'poster')


class CreateChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ('name', 'private')
